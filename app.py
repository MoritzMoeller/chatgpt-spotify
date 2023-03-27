from flask import Flask, request, render_template, redirect, session
from flask_session import Session
from create_playlist import create_playlist
from query_gpt import query_gpt
import spotipy

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign_in')
def sign_in():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    # Coming back from from Spotify auth page
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return render_template('generate.html')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(auth_manager.get_authorize_url())

    return render_template('generate.html')


@app.route('/generate', methods=['POST'])
def generate():
    # Query ChatGPT
    print("Start generation process ...")
    playlist_description = request.form["description"]
    print("Description ingested ...\n'{}'".format(playlist_description))
    content = query_gpt(query=playlist_description)
    print("Content retrieved ...")
    print("Title: '{}'".format(content["title"]))

    # Log into spotify
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/sign_in')

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Create playlist
    playlist_address = create_playlist(content["title"], playlist_description, content["songs"], spotify)
    return redirect(playlist_address)


if __name__ == "__main__":
    app.run()
