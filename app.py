from flask import Flask, request, render_template, redirect, session
from flask_session import Session
from create_playlist import create_playlist
from query_gpt import query_gpt
import spotipy
import os

app = Flask(__name__)

# create key to sign cookies with session id
app.config['SECRET_KEY'] = os.urandom(64)

# set up session data to be stored in file system
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

# Set some global variables
username = 'epic_playlist_generator'
scope = 'playlist-modify-public'

# create flask-session
Session(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    cache_handler = spotipy.cache_handler.CacheFileHandler(username=username)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    # Arrive from Spotify authentification
    if request.args.get('code'):
        auth_manager.get_access_token(request.args.get('code'))

    # if not yet authorized, send to authorization
    # TODO: Could add check whether the correct account is authorized
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(auth_manager.get_authorize_url())

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    account_address = spotify.me()['external_urls']['spotify']
    return redirect(account_address)


@app.route('/generate', methods=['POST'])
def generate():
    cache_handler = spotipy.cache_handler.CacheFileHandler(username=username)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    # Arrive from landing page via button
    session['playlist_description'] = request.form["description"]

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return render_template('not_logged_in.html')

    # Query ChatGPT
    playlist_description = session['playlist_description']
    content = query_gpt(query=playlist_description)

    # Create playlist
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlist = create_playlist(content["title"], playlist_description, content["songs"], spotify)
    return redirect(playlist['url'])


@app.route('/get_link', methods=['POST'])
def get_link():

    cache_handler = spotipy.cache_handler.CacheFileHandler(username=username)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return render_template('not_logged_in.html')

    # Unpack description
    content = request.get_json()
    session['playlist_description'] = content['description']

    # Query ChatGPT
    playlist_description = session['playlist_description']
    content = query_gpt(query=playlist_description)

    # Create playlist
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlist = create_playlist(content["title"], playlist_description, content["songs"], spotify)

    link = {'link': playlist["url"], 'success': playlist["success"]}
    return link


if __name__ == "__main__":
    app.run()
