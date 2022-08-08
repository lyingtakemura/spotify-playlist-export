from spotify import Spotify

spotify = Spotify()
playlist = spotify.get_playlist()
spotify.export_to_csv(playlist)
