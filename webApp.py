from flask import Flask, redirect, request, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from collections import Counter
import json
import pandas as pd
import random  # Import the random module

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'user-top-read'  # Add or modify scopes as needed

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE)

# Load the genre to broad genre mapping
with open('/Users/rdas/Desktop/DemoTest/rhythmoji/testGenres.json', 'r') as file:
    genre_to_broad_genre = json.load(file)

# Load the broad genre to fashion items mapping
genre_clothing_styles_df = pd.read_csv('/Users/rdas/Desktop/DemoTest/rhythmoji/genre_clothing_styles_updatd.csv')
genre_clothing_styles_df.set_index('Unnamed: 0', inplace=True)

def map_genres_to_fashion_items(genre_counts):
    # Get top 10 genres with counts
    top_genres = [genre[0] for genre in genre_counts.most_common(10)]  # Extract genre names without counts
    print(f"Top 10 genres: {top_genres}")

    # Map to broad genres and fashion items
    genre_fashion_mapping = {}
    for genre in top_genres:
        matched = False
        for broad_genre, subgenres in genre_to_broad_genre.items():
            if genre in subgenres:
                try:
                    fashion_items = genre_clothing_styles_df.loc[broad_genre].to_dict()
                    genre_fashion_mapping[genre] = {
                        'broad_genre': broad_genre,
                        'fashion_items': fashion_items,
                        'count': genre_counts[genre]  # Include the count in the mapping
                    }
                    matched = True
                    break
                except KeyError as e:
                    print(f"KeyError for broad genre '{broad_genre}': {e}")
        if not matched:
            print(f"No broad genre match for '{genre}'")

    if not genre_fashion_mapping:
        print("No genres were mapped to fashion items.")
    else:
        print(f"Genre to fashion mapping: {genre_fashion_mapping}")

    return genre_fashion_mapping



def assign_clothing_items(genre_fashion_mapping):
    # Clothing categories in order of importance
    clothing_categories = ['Shirts', 'Shoes', 'Pants', 'Headwear', 'Accessories']
    
    # Assign items based on weights (listening frequency)
    assigned_items = {}
    for category in clothing_categories:
        # Find the genre with the highest count still unassigned
        top_genre = max(genre_fashion_mapping, key=lambda g: genre_fashion_mapping[g]['count'] if g not in assigned_items else 0)
        
        # Assign a random item from the category
        if top_genre:
            items = genre_fashion_mapping[top_genre]['fashion_items'][category].split(', ')
            assigned_items[top_genre] = random.choice(items)

    return assigned_items

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/get_user_genre_data')

@app.route('/get_user_genre_data')
def get_user_genre_data():
    token_info = session.get('token_info', None)

    if not token_info:
        print("No token info found in session.")
        return redirect('/login')  # Redirect to login route if not authenticated

    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    try:
        top_artists = sp.current_user_top_artists(limit=50, time_range='short_term')
    except Exception as e:
        print(f"Error fetching top artists: {e}")
        return "Error fetching data from Spotify"

    genres = [artist['genres'] for artist in top_artists['items']]
    if not genres:
        print("No genres found in top artists data.")
        return "No genres data available"

    flattened_genres = [genre for sublist in genres for genre in sublist]

    if not flattened_genres:
        print("No genres found after flattening.")
        return "No genres data available after flattening"

    genre_counts = Counter(flattened_genres)
    if not genre_counts:
        print("Genre counts are empty.")
        return "No genre counts available"

    genre_fashion_mapping = map_genres_to_fashion_items(genre_counts)
    if not genre_fashion_mapping:
        print("Genre to fashion mapping is empty.")
        return "No genre to fashion mapping available"

    # Assign clothing items based on the weight-based system
    assigned_clothing = assign_clothing_items(genre_fashion_mapping)

    # Rendering the genre to fashion mapping and assigned clothing on a webpage
    return render_template('genre_display.html', genre_fashion_mapping=genre_fashion_mapping, assigned_clothing=assigned_clothing)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
