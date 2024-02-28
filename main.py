import logging
import os
from time import perf_counter

import httpx
from dotenv import load_dotenv

from config.auth import get_headers
from config.save_as import save_as_json

load_dotenv()

logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.CRITICAL,
)


playlist_id = os.getenv("PLAYLIST_ID")
urls = [f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks/"]
client = httpx.Client(headers=get_headers())
results = []


def get_playlist_urls(url: str = urls[0]):
    response = client.get(url)
    response = response.json()

    if response["next"]:
        urls.append(response["next"])
        get_playlist_urls(response["next"])


def parse_playlist():
    for url in urls:
        response = client.get(url).json()["items"]

        for item in response:
            results.append(
                {
                    "album": item["track"]["album"]["name"],
                    "artists": item["track"]["artists"][0]["name"],
                    "name": item["track"]["name"],
                }
            )


def main():
    get_playlist_urls()
    parse_playlist()
    save_as_json("sync_result", results)


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    time = end - start
    print(f"SYNC RUN TOOK: {time}")
