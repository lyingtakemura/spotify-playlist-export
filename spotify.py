import csv
import os
from base64 import b64encode

import requests
from dotenv import load_dotenv

load_dotenv()


class Spotify:
    def __init__(self):
        self.url = os.getenv("URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.playlist = None

    @property
    def headers(self):
        _ = {
            "Authorization": "Bearer {}".format(
                self.access_token
            ),
            "grant_type": "access_token"
        }
        return _

    @property
    def access_token(self):
        """
        - encode client_id and client_secret to base64 string
        - request spotify api access_token by resulted base64 string
        """
        b64string = "{}:{}".format(self.client_id, self.client_secret)
        b64string = b64string.encode("ASCII")
        b64string = b64encode(b64string)
        b64string = bytes.decode(b64string)

        headers = {
            "Authorization": "Basic {}".format(b64string)
        }
        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data=data
        )
        result = response.json()
        return result["access_token"]

    def get_playlist_by_url(self) -> None:
        """
        - stay in the loop until provided input can be parsed for playlist id
        - request spotify api for playlist with parsed id
        - if playlist found - set response json as spotify.playlist attribute
        """
        while True:
            try:
                playlist_url = input("ENTER PLAYLIST URL: ")
                playlist_id = playlist_url.split("/playlist/")[1]
                playlist_id = playlist_id.split("?")[0]
                # handle playlist with provided id not found
                url = "{}/playlists/{}/tracks/".format(
                    self.url, playlist_id
                )
                response = requests.get(url, headers=self.headers)
                self.playlist = response.json()
                # raise HTTPError if response returned an error status code
                response.raise_for_status()
                break
            except IndexError:
                print("ERROR: Invalid playlist URL")
            except requests.HTTPError as error:
                print("ERROR: {}".format(error))

    def parse_playlist_tracks(self) -> None:
        """
        - check if playlist has link to 'next' part
        - if 'next' is None: end of playlist reached, exit loop
        """
        result = []
        while True:
            result.extend(self.playlist["items"])
            if self.playlist["next"] is None:
                break
            else:
                url = self.playlist["next"]
                self.playlist = requests.get(url, headers=self.headers).json()

        self.playlist = result

    def export_to_csv(self) -> None:
        with open("playlist.csv", "w") as file:
            writer = csv.writer(file)

            for item in self.playlist:
                name = item["track"]["name"]

                artists = []
                for artist in item["track"]["artists"]:
                    artists.append(artist["name"])
                artists = ", ".join(artists)

                album = item["track"]["album"]["name"]

                writer.writerow([name, artists, album])
