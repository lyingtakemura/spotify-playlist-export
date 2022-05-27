from spotify import Spotify

spotify = Spotify()

playlist = spotify.get_playlist(playlist_id="")
print(playlist)
