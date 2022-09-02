from spotify import ExportToCSV, ExportToJSON, Spotify

spotify = Spotify()
spotify.get_playlist()
spotify.export_playlist(ExportToCSV())
spotify.export_playlist(ExportToJSON())
