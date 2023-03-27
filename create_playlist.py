import spotipy
from spotipy.oauth2 import SpotifyOAuth


def create_playlist(playlist_name, playlist_description, songs, sp):
    # authenticate
    print("Authenticate at spotify ...")

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)


    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # search for songs on spotify and build list
    items_to_add = []
    for song in songs:
        if song:
            print("Querying for song ...\n{}".format(song))
            spotify_result = sp.search(q=song, type="track")
            song_uri = spotify_result['tracks']['items'][0]['uri']
            if song_uri:
                print("Adding spotify URI for song ...\n{}".format(song_uri))
                items_to_add.append(song_uri)
            else:
                print("Song not found ...")

    # create playlist
    print("Creating playlist ...")
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
