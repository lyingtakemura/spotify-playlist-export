from spotify import Spotify

spotify = Spotify()
spotify.get_playlist_by_url()
spotify.parse_playlist_tracks()
spotify.export_to_csv()
