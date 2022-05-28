from spotify import Spotify

spotify = Spotify()
playlist = spotify.get_playlist(playlist_url="")
spotify.export_to_csv(playlist)
