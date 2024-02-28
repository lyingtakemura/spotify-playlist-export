import asyncio
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

client = httpx.AsyncClient(headers=get_headers())
results = []


async def get_playlist_urls(url: str = urls[0]):
    try:
        response = await client.get(url)
        response = response.json()

        if response["next"]:
            urls.append(response["next"])
            await get_playlist_urls(response["next"])

    except Exception as e:
        print(e)


async def parse_playlist(url: str) -> list:
    try:
        response = await client.get(url)
        response = response.json()["items"]

        for item in response:
            results.append(
                {
                    "album": item["track"]["album"]["name"],
                    "artists": item["track"]["artists"][0]["name"],
                    "name": item["track"]["name"],
                }
            )
    except Exception as e:
        print(e)


async def main():
    await get_playlist_urls()
    await asyncio.gather(*[parse_playlist(url) for url in urls])
    save_as_json("async_result", results)


if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(main())
    end = perf_counter()
    time = end - start
    print(f"ASYNC RUN TOOK: {time}")
