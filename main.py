import csv
import json
import logging
import os
from base64 import b64encode
from datetime import datetime

import requests
from dotenv import load_dotenv

from time import perf_counter

load_dotenv()
logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        time = end - start
        print("{} RUN TOOK: {}".format(func.__name__.upper(), time))
        return result

    return wrapper


class Spotify:
    def __init__(self):
        self.url = os.getenv("URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.playlist = []

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

        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        return result["access_token"]

    @property
    def headers(self) -> dict:
        _ = {
            "Authorization": "Bearer {}".format(self.authenticate),
            "grant_type": "access_token",
        }
        return _

    def playlist_filepath(self) -> str:
        path = "{}/playlists/".format(os.getcwd())
        if not os.path.exists(path):
            os.mkdir(path)

        date = datetime.now().date()
        time = datetime.now().time().replace(microsecond=0)
        filename = "{}_{}".format(date, time)
        return "{}/{}".format(path, filename)

    @benchmark
    def request_playlist(self) -> dict:
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

                if not response.raise_for_status():
                    response = response.json()

                self.playlist.extend(response["items"])

                while True:
                    if response["next"] is None:
                        break
                    else:
                        response = requests.get(
                            response["next"], headers=self.headers
                        ).json()
                        self.playlist.extend(response["items"])

                break
            except IndexError:
                print("ERROR: PROVIDED URL IS INVALID")
            except requests.HTTPError as error:
                print("ERROR: {}".format(error))

    @benchmark
    def parse_playlist(self) -> None:
        result = []
        for item in self.playlist:
            artists = []
            for artist in item["track"]["artists"]:
                artists.append(artist["name"])
            artists = ", ".join(artists)

            name = item["track"]["name"]
            album = item["track"]["album"]["name"]

            track = (name, artists, album)
            result.append(track)
        self.playlist = result

    def export_to_csv(self) -> None:
        with open(self.playlist_filepath() + ".csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows([item for item in self.playlist])

    def export_to_json(self) -> None:
        result = []
        for item in self.playlist:
            result.append({"name": item[0], "artists": item[1], "album": item[2]})
        result = json.dumps(result, indent=4)

        with open(self.playlist_filepath() + ".json", "w") as file:
            file.writelines(result)


def main():
    try:
        _ = Spotify()
        _.request_playlist()
        _.parse_playlist()
        _.export_to_csv()
        _.export_to_json()
    except KeyboardInterrupt:
        print("\nINTERRUPTED")


if __name__ == "__main__":
    logging.debug(main)
    main()
