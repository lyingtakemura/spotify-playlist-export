import csv
import json
import os
from abc import ABC, abstractmethod
from base64 import b64encode
from datetime import datetime

import requests
from dotenv import load_dotenv

from utils import timeit

load_dotenv()


class ExportStrategy(ABC):
    @abstractmethod
    def process(self, items: list):
        pass


class ExportToCSV(ExportStrategy):
    def process(self, items: list):
        with open(os.getcwd() + _set_playlist_path() + ".csv", "w") as file:
            writer = csv.writer(file)

            for item in items:
                name = item["track"]["name"]

                artists = []
                for artist in item["track"]["artists"]:
                    artists.append(artist["name"])
                artists = ", ".join(artists)

                album = item["track"]["album"]["name"]

                writer.writerow([name, artists, album])
            print("EXPORTED TO CSV...")


class ExportToJSON(ExportStrategy):
    def process(self, items: list):
        with open(os.getcwd() + _set_playlist_path() + ".json", "w") as file:
            result = []
            for item in items:
                obj = {"name": None, "artists": None, "album": None}
                obj["name"] = item["track"]["name"]

                artists = []
                for artist in item["track"]["artists"]:
                    artists.append(artist["name"])
                obj["artists"] = ", ".join(artists)

                obj["album"] = item["track"]["album"]["name"]

                result.append(obj)
            result = json.dumps(result, indent=4)
            file.writelines(result)
            print("EXPORTED TO JSON...")


def _set_playlist_path():
    now = datetime.now()
    path = "{}_{}".format(now.date(), now.time().replace(microsecond=0))
    return "/playlists/{}".format(path)


class Spotify:
    def __init__(self):
        self.url = os.getenv("URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.playlist = {"items": [], "total": None}

        # OUTPUT DIR SETUP
        path = "{}/playlists/".format(os.getcwd())
        if not os.path.exists(path):
            os.mkdir(path)
            print("OUTPUT DIR SETUP...")

    @property
    def authenticate(self) -> str:
        """
        - encode client_id and client_secret to base64 string
        - request spotify api access_token by resulted base64 string
        """
        b64string = "{}:{}".format(self.client_id, self.client_secret)
        b64string = b64string.encode("ASCII")
        b64string = b64encode(b64string)
        b64string = bytes.decode(b64string)

        headers = {"Authorization": "Basic {}".format(b64string)}
        data = {"grant_type": "client_credentials"}

        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )
        result = response.json()
        return result["access_token"]

    @property
    def headers(self) -> dict:
        _ = {
            "Authorization": "Bearer {}".format(self.authenticate),
            "grant_type": "access_token",
        }
        return _

    def get_playlist(self) -> dict:
        """
        - stay in the loop until provided input can be parsed for playlist id
        - request spotify api for playlist with parsed id
        - if exists - save response object to 'result' variable
        - check if playlist has link to 'next' part
        - if 'next' is None: end of playlist reached, exit loop
        """
        while True:
            try:
                playlist_url = input("ENTER PLAYLIST URL: ")
                playlist_id = playlist_url.split("/playlist/")[1]
                playlist_id = playlist_id.split("?")[0]

                url = "{}/playlists/{}/tracks/".format(self.url, playlist_id)
                response = requests.get(url, headers=self.headers)

                # raise HTTPError if request failed
                if not response.raise_for_status():
                    playlist = response.json()

                # with open("temp.json", "w") as file:
                #     json.dump(playlist, file, indent=4)

                self.playlist["total"] = playlist["total"]
                self.playlist["items"].extend(playlist["items"])

                while True:
                    if playlist["next"] is None:
                        break
                    else:
                        playlist = requests.get(
                            playlist["next"], headers=self.headers
                        ).json()
                        self.playlist["items"].extend(playlist["items"])
                break
            except IndexError:
                print("ERROR: Invalid playlist URL")
            except requests.HTTPError as error:
                print("ERROR: {}".format(error))

    @timeit
    def export_playlist(self, strategy: ExportStrategy) -> None:
        return strategy.process(self.playlist["items"])
