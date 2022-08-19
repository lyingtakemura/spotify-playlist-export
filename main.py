from spotify import Spotify

spotify = Spotify()
playlist = spotify.request_playlist_tracks()
spotify.export_to_csv(playlist)
