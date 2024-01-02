import json
import logging
import os
from base64 import b64encode
from time import perf_counter

import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)

URLS = []
PLAYLIST_ID = ""


def authenticate() -> dict:
    """
    - encode client_id and client_secret to base64 string
    - request spotify api access_token by base64 string
    """
    b64string = "{}:{}".format(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
    b64string = b64string.encode("ASCII")
    b64string = b64encode(b64string)
    b64string = bytes.decode(b64string)

    headers = {"Authorization": "Basic {}".format(b64string)}
    data = {"grant_type": "client_credentials"}

    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, headers=headers, data=data).json()
    return {
        "Authorization": "Bearer {}".format(response["access_token"]),
        "grant_type": "access_token",
    }


def session():
    session = requests.session()
    session.headers.update(authenticate())
    return session


def get_playlist_urls(session, url):
    while True:
        response = session().get(url).json()

        if not response["next"]:
            break

        URLS.append(response["next"])
        url = response["next"]


def parse_playlist(session, url):
    response = session().get(url).json()
    with open("SYNC_RESULT.json", "a") as file:
        file.writelines(json.dumps(response["items"], indent=4))


def main():
    get_playlist_urls(
        session, "https://api.spotify.com/v1/playlists/{}/tracks/".format(PLAYLIST_ID)
    )

    for url in URLS:
        parse_playlist(session, url)


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    time = end - start
    print("SYNC RUN TOOK: {}".format(time))
