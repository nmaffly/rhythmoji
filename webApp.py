from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

client_id = 'abcdc6ec5e66488ab295abb3a4401917'
client_secret = '9ed30e1571364288b2a8a1b690f2ea91'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback', scope='user-library-read user-top-read'))
user = sp.current_user()
top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')


app = Flask(__name__)

@app.route('/')
def show_top_tracks():
    html_content = generate_html()
    return render_template('index.html', content=html_content)

def generate_html():
    html_content = f"<h1>Welcome, {user['display_name']}!"
    for idx, track in enumerate(top_tracks['items']):
        track_info = f"{idx + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
        html_content += f"<p>{track_info}</p>"

    return html_content


if __name__ == '__main__':
    app.run(debug=True)
    
    