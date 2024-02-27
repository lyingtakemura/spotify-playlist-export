import asyncio
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
client = httpx.AsyncClient(headers=get_headers())


async def get_playlist_urls(url):
    while True:
        response = await client.get(url)
        response = response.json()

        if not response["next"]:
            break

        urls.append(response["next"])
        url = response["next"]


async def parse_playlist(url):
    response = await client.get(url)
    response = response.json()

    with open("ASYNC_RESULT.json", "a") as file:
        file.writelines(json.dumps(response["items"], indent=4))


async def main():
    await get_playlist_urls(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks/"
    )
    await asyncio.gather(*[parse_playlist(url) for url in urls])


if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(main())
    end = perf_counter()
    time = end - start
    print("ASYNC RUN TOOK: {}".format(time))
