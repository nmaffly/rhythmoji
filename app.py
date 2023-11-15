from flask import Flask, redirect, request, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your_new_random_secret_here'  # Change to a strong, unique key

# Load environment variables
load_dotenv()

# Spotify OAuth settings
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
    return redirect('/get_top_artists')

@app.route('/get_top_artists')
def get_top_artists():
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            raise Exception("User not logged in")
        sp = spotipy.Spotify(auth=token_info['access_token'])
        top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
        return render_template('top_artists.html', top_artists=top_artists['items'])
    except Exception as e:
        print(e)
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8888)
