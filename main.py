import requests

from spotify import Spotify

spotify = Spotify()

url = "https://api.spotify.com/v1/playlists/{}/tracks"
headers = {
    "Authorization": "Bearer {}".format(spotify.get_access_token()),
    "grant_type": "access_token"
}
response = requests.get(url, headers=headers)
print(response.text)
