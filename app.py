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
    content = query_gpt(query=playlist_description)
    print("Content retrieved ...")
    print("Title: '{}'".format(content["title"]))
    playlist_address = create_playlist(content["title"], playlist_description, content["songs"])
    return redirect(playlist_address)


if __name__ == "__main__":
    app.run()
