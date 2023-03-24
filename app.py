from flask import Flask, request, render_template, redirect
from create_playlist import create_playlist, create_test_playlist
from query_gpt import test_query_gpt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        playlist_content = test_query_gpt()
        playlist_name = "Test2"
        playlist_description = "TEst playlist 2"
        playlist_address= create_playlist(playlist_name, playlist_description, playlist_content)
        return redirect(playlist_address)
    else:
        return "Only POST requests are allowed for this route."


if __name__ == "__main__":
    app.run()
