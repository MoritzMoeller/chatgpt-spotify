from flask import Flask, request, render_template, redirect
from create_playlist import create_playlist
from query_gpt import query_gpt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    print("Start generation process ...")
    playlist_description = request.form["description"]
    print("Description ingested ...\n'{}'".format(playlist_description))
    playlist_content = query_gpt(query=playlist_description)
    print("Content retrieved ...\n'{}'".format(playlist_content))
    playlist_name = "Test_full"
    playlist_address = create_playlist(playlist_name, playlist_description, playlist_content)
    return redirect(playlist_address)


if __name__ == "__main__":
    app.run()
