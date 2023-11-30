from flask import Flask, redirect, request, session, render_template, g
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from collections import Counter
from retrieve_broad_genre import genre_lookup_table, get_broad_genre
import pandas as pd
import time
import random

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'user-library-read user-top-read'

sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)

#Load genre_to_clothing csv into data frame
current_directory = os.getcwd()
file_path = os.path.join(current_directory, 'genre_to_clothing.csv')
genre_to_clothing_df = pd.read_csv(file_path)

#Before request (delete later)
@app.before_request
def before_request():
    g.start_time = time.time()

# After request for testing website response times to requests (delete later)
@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        elapsed_time = time.time() - g.start_time
        app.logger.info(f"Request took {elapsed_time:.5f} seconds")
    return response


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
    return redirect('/get_top_genres')

@app.route('/get_top_genres')
def get_top_genres():
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            raise Exception("User not logged in")
        sp = spotipy.Spotify(auth=token_info['access_token'])
        top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')['items']
        genres = extract_genres(sp, top_artists)
        top_genres = Counter(genres).most_common(10)

        broad_genres = categorize_subgenres(top_genres)

        assigned_clothing = assign_clothing(broad_genres)

        new_assigned_clothing = generate_avatar(assigned_clothing)
        

        print(assigned_clothing)
        
        return render_template('top_genres.html', top_genres=top_genres, broad_genres=broad_genres, assigned_clothing=new_assigned_clothing)
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        return redirect('/')

# Picks clothing from csv table
def generate_avatar(assigned_clothing):
    new_assigned_clothing = []

    for i, (clothes, genre) in enumerate(assigned_clothing):
        result = genre_to_clothing_df[genre_to_clothing_df['Genres'] == genre][clothes].values
        if len(result) > 0:
            result_list = result[0].split(', ')
            random_clothing = random.choice(result_list)
            clothing_and_genre = [clothes, random_clothing, genre]
            new_assigned_clothing.append(clothing_and_genre)

    return new_assigned_clothing 
            

# Sort a user's specific top genres into broader genres
# Returns list of tuples where each tuple is (broad genre, amount they listen to this genre)
def categorize_subgenres(top_genres):
    broad_genres = []
    for genre in top_genres:
        broad_genre = get_broad_genre(genre[0], genre_lookup_table)
        broad_genre_tuple = (broad_genre, genre[1])

        genre_exists = False

        for i, (_genre, _count) in enumerate(broad_genres):
            if _genre == broad_genre_tuple[0]:
                # Update the count in the tuple
                broad_genres[i] = (_genre, _count + broad_genre_tuple[1])
                genre_exists = True
                break  # Break the loop once the update is done
                
        if not genre_exists:
            broad_genres.append(broad_genre_tuple)

    return get_category_proporions(broad_genres)

# Changes number to a percentage in the list of tuples of broad genres
def get_category_proporions(broad_genres):
    total = sum(genre[1] for genre in broad_genres)
    
    for i, genre in enumerate(broad_genres):
        percentage = round((genre[1] / total) * 100)
        broad_genres[i] = (genre[0], percentage)

    broad_genres = sorted(broad_genres, key=lambda x: x[1], reverse=True)
    print(broad_genres)

    return broad_genres

# Assigns each genre to a clothing item depending on how many broad genres a user listens to
# and what their top genres are 
def assign_clothing(broad_genres):
    clothing_categories = ['Shirts', 'Shoes', 'Pants', 'Headwear', 'Accessories']

    assigned_items = []

    if len(broad_genres) == 1:
        top_genre = broad_genres[0][0]
        assigned_items = [('Shirts', top_genre), ('Shoes', top_genre),
                          ('Pants', top_genre), ('Headwear', top_genre),
                          ('Accessories', top_genre)]
    elif len(broad_genres) == 2:
        assigned_items = [('Shirts', broad_genres[0][0]), ('Shoes', broad_genres[0][0]),
                          ('Headwear', broad_genres[0][0]), ('Pants', broad_genres[1][0]),
                          ('Accessories', broad_genres[1][0])]
    elif len(broad_genres) == 3:
        assigned_items = [('Shirts', broad_genres[0][0]), ('Shoes', broad_genres[0][0]),
                          ('Headwear', broad_genres[1][0]), ('Pants', broad_genres[1][0]),
                          ('Accessories', broad_genres[2][0])]
    elif len(broad_genres) == 4:
        assigned_items = [('Shirts', broad_genres[0][0]), ('Shoes', broad_genres[0][0]),
                          ('Headwear', broad_genres[1][0]), ('Pants', broad_genres[2][0]),
                          ('Accessories', broad_genres[3][0])]
    else:
        assigned_items = [('Shirts', broad_genres[0][0]), ('Shoes', broad_genres[1][0]),
                          ('Headwear', broad_genres[2][0]), ('Pants', broad_genres[3][0]),
                          ('Accessories', broad_genres[4][0])]

    return assigned_items

def extract_genres(sp, top_artists):
    genres = []
    for artist in top_artists:
        artist_genres = sp.artist(artist['id'])['genres']
        genres.extend(artist_genres)
    return genres

if __name__ == '__main__':
    app.run(debug=True, port=8888)
