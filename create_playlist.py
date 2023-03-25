import spotipy
from spotipy.oauth2 import SpotifyOAuth


def create_playlist(playlist_name, playlist_description, playlist_content):
    # authenticate
    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

    # parse song list
    song_list = playlist_content.split(", ")

    # search for songs on spotify and build list
    items_to_add = []
    for song in song_list:
        if song:
            spotify_result = sp.search(q=song, type="track")
            print(song)
            items_to_add.append(spotify_result['tracks']['items'][0]['uri'])
            print(spotify_result['tracks']['items'][0]['uri'])

    # create playlist
    user_data = sp.current_user()
    my_playlist = sp.user_playlist_create(user=user_data['id'],
                                          name=playlist_name,
                                          public=False,
                                          description=playlist_description)

    # add songs to playlist
    sp.playlist_add_items(playlist_id=my_playlist['id'], items=items_to_add)

    return my_playlist['external_urls']['spotify']


def create_test_playlist():
    playlist_content = "Estate - Giuni Russo, Amore Disperato - Nada, Se Telefonando - Mina, Luna Per Te - Vasco " \
                       "Rossi, Tutta Mia La Città - Bruno Martino, Acqua e Sapone - Stadio, Io E Te Da Soli - Matia " \
                       "Bazar, Felicità - Al Bano & Romina Power, Sarà Perché Ti Amo - Ricchi e Poveri, " \
                       "Alice - Franco Battiato "
    playlist_name = "test_playlist"
    playlist_description = "Testing automatic playlist generation"

    return create_playlist(playlist_name, playlist_description, playlist_content)
