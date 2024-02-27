import json
import logging
import os
from time import perf_counter

import httpx
from dotenv import load_dotenv

from auth import get_headers

load_dotenv()

logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)


urls = []
playlist_id = os.getenv("PLAYLIST_ID")
client = httpx.Client(headers=get_headers())


def get_playlist_urls(url):
    while True:
        response = client.get(url)
        response = response.json()

        if not response["next"]:
            break

        urls.append(response["next"])
        url = response["next"]


def parse_playlist(url):
    response = client.get(url).json()
    with open("SYNC_RESULT.json", "a") as file:
        file.writelines(json.dumps(response["items"], indent=4))


def main():
    get_playlist_urls(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks/")

    for url in urls:
        parse_playlist(url)


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    time = end - start
    print(f"SYNC RUN TOOK: {time}")
