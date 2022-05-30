from spotify import Spotify

spotify = Spotify()
playlist = spotify.get_playlist(playlist_url=input("Enter playlist url: "))
spotify.export_to_csv(playlist)
