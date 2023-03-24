import csv
import json
import logging
import os
from base64 import b64encode

import requests
from dotenv import load_dotenv

from utils import timeit

load_dotenv()
logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)


class Spotify:
    def __init__(self):
        self.url = os.getenv("URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.playlist = {"items": []}

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

    @property
    def playlist_filepath(self) -> str:
        from datetime import datetime

        path = "{}/playlists/".format(os.getcwd())
        if not os.path.exists(path):
            os.mkdir(path)
            print("OUTPUT DIR SETUP...")

        now = datetime.now()
        filename = "{}_{}".format(now.date(), now.time().replace(microsecond=0))
        return "{}/{}".format(path, filename)

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

                # raise HTTPError if request failed
                if not response.raise_for_status():
                    playlist = response.json()

                # with open("temp.json", "w") as file:
                #     json.dump(playlist, file, indent=4)

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

    def parse_playlist(self) -> None:
        result = []
        for item in self.playlist["items"]:

            artists = []
            for artist in item["track"]["artists"]:
                artists.append(artist["name"])
            artists = ", ".join(artists)

            track = (item["track"]["name"], artists, item["track"]["album"]["name"])
            result.append(track)
        self.playlist["items"] = result

    @timeit
    def export_to_csv(self) -> None:
        with open(self.playlist_filepath + ".csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows([item for item in self.playlist["items"]])

    @timeit
    def export_to_json(self) -> None:
        result = []
        for item in self.playlist["items"]:
            result.append({"name": item[0], "artists": item[1], "album": item[2]})
        result = json.dumps(result, indent=4)

        with open(self.playlist_filepath + ".json", "w") as file:
            file.writelines(result)


def main():
    try:
        spotify = Spotify()
        spotify.request_playlist()
        spotify.parse_playlist()
        spotify.export_to_csv()
        spotify.export_to_json()

        # if "--csv" in sys.argv:
        #     spotify.export_to_csv()

        # if "--json" in sys.argv:
        #     spotify.export_playlist(ExportToJSON())

    except KeyboardInterrupt:
        print("\nINTERRUPTED")


if __name__ == "__main__":
    logging.debug(main)
    main()
