import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

client_id = 'abcdc6ec5e66488ab295abb3a4401917'
client_secret = '9ed30e1571364288b2a8a1b690f2ea91'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback', scope='user-library-read user-top-read'))

user = sp.current_user()
print(f"Welcome, {user['display_name']}!")

top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')
print("\nYour Top Tracks:")
for idx, track in enumerate(top_tracks['items']):
    print(f"{idx + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
