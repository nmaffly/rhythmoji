from flask import Flask, redirect, request, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from collections import Counter
from genre_fashion_mapping import genre_fashion  # Import the genre-fashion mapping

app = Flask(__name__)
app.secret_key = 'your_new_random_secret_here'

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'user-top-read'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/get_top_genres')


def generate_avatar_description(top_genres):
    avatar_description = []
    for genre, _ in top_genres:
        fashion_items = genre_fashion.get(genre.lower(), [])
        avatar_description.extend(fashion_items)
    return avatar_description


@app.route('/get_top_genres')
def get_top_genres():
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            raise Exception("User not logged in")
        sp = spotipy.Spotify(auth=token_info['access_token'])
        # Changed time_range to 'short_term' for the last month
        top_artists = sp.current_user_top_artists(limit=50, time_range='short_term')['items']
        genres = extract_genres(sp, top_artists)
        top_genres = Counter(genres).most_common(10)
        
        # Call the function to generate the avatar description
        avatar_description = generate_avatar_description(top_genres)
        
        return render_template('top_genres.html', top_genres=top_genres, avatar_description=avatar_description)
    except Exception as e:
        print(e)
        return redirect('/')

def generate_clothing_items(top_genres):
    clothing_items = []
    for genre, _ in top_genres:
        fashion_items = genre_fashion.get(genre.lower(), [])
        print(f"Genre: {genre}, Fashion Items: {fashion_items}")
        clothing_items.extend(fashion_items)
    return clothing_items

def extract_genres(sp, top_artists):
    genres = []
    for artist in top_artists:
        artist_genres = sp.artist(artist['id'])['genres']
        genres.extend(artist_genres)
    return genres

if __name__ == '__main__':
    app.run(debug=True, port=8888)
