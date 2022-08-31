from spotify import ExportToCSVStrategy, ExportToJsonStrategy, Spotify

spotify = Spotify()
spotify.get_playlist()
spotify.export_playlist(ExportToCSVStrategy())
spotify.export_playlist(ExportToJsonStrategy())
