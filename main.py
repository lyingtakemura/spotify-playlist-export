from spotify import Spotify

spotify = Spotify()
spotify.verify_playlist_id()
spotify.parse_playlist_tracks()
spotify.export_to_csv()
