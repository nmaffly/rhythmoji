import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Explicitly clear the cache (if exists)
cache_file = ".cache"
if os.path.exists(cache_file):
    os.remove(cache_file)

# Set up Spotify client with OAuth without using cache
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='user-top-read',
    cache_path=None  # Disable caching by setting cache_path to None
))

# Fetch the current user's profile
user = sp.current_user()
print(f"Welcome, {user['display_name']}!")

# Fetch the current user's top artists
top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
print("\nYour Top Artists:")
for idx, artist in enumerate(top_artists['items']):
    print(f"{idx + 1}. {artist['name']}")

# Add any additional functionality you need here
