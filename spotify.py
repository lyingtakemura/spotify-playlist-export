import csv
import os
from base64 import b64encode

import requests
from dotenv import load_dotenv

load_dotenv()


class Spotify:
    def __init__(self):
        self.url = "https://api.spotify.com/v1"
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

    def __get_access_token(self) -> str:
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

    def __find_playlist(self) -> str:
        """
        stay in the loop until provided input can be parsed for playlist id
        then make api request to check if playlist with provided id exists
        """
        playlist_id = None
        while True:
            try:
                # parse playlist id from input
                playlist_url = input("ENTER PLAYLIST URL: ")
                playlist_id = playlist_url.split("/playlist/")[1]
                playlist_id = playlist_id.split("?")[0]
                # handle playlist with provided id not found
                url = "{}/playlists/{}/tracks".format(self.url, playlist_id)
                headers = {
                    "Authorization": "Bearer {}".format(
                        self.__get_access_token()
                    ),
                    "grant_type": "access_token"
                }
                response = requests.get(url, headers=headers)
                # raise HTTPError if response
                # returned an unsuccessful status code
                response.raise_for_status()
                break
            except IndexError:
                print("ERROR: Invalid playlist URL")
            except requests.HTTPError:
                print("ERROR: Playlist with provided id not found")

        return playlist_id

    def get_playlist(self) -> list:
        """
        - parse playlist_id from provided playlist_url
        - construct initial request url
        - request first 100 songs from playlist and check if response attribute
        'next' has link to the next part of playlist
        - if 'next' is None: end of playlist reached, exit loop
        """
        result = []

        url = "{}/playlists/{}/tracks".format(
            self.url,
            self.__find_playlist()
        )
        headers = {
            "Authorization": "Bearer {}".format(self.__get_access_token()),
            "grant_type": "access_token"
        }

        while True:
            response = requests.get(url, headers=headers).json()
            result.extend(response["items"])

            if response["next"] is None:
                break
            else:
                url = response["next"]

        return result

    def export_to_csv(self, playlist: list) -> None:
        with open("playlist.csv", "w") as file:
            writer = csv.writer(file)

            for item in playlist:
                name = item["track"]["name"]

                artists = []
                for artist in item["track"]["artists"]:
                    artists.append(artist["name"])
                artists = ", ".join(artists)

                album = item["track"]["album"]["name"]

                writer.writerow([name, artists, album])
