import asyncio
import json
import logging
import os
from base64 import b64encode
from time import perf_counter

import aiohttp
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)

urls = []
result = []
PLAYLIST_ID = ""


async def authenticate():
    async with aiohttp.ClientSession() as session:
        b64string = "{}:{}".format(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
        b64string = b64string.encode("ASCII")
        b64string = b64encode(b64string)
        b64string = bytes.decode(b64string)

        headers = {"Authorization": "Basic {}".format(b64string)}
        data = {"grant_type": "client_credentials"}

        url = "https://accounts.spotify.com/api/token"
        async with session.post(url, headers=headers, data=data) as response:
            result = await response.json()

        return {
            "Authorization": "Bearer {}".format(result["access_token"]),
            "grant_type": "access_token",
        }


async def get_playlist_urls(session, url):
    while True:
        async with session.get(url) as response:
            data = await response.json()

        if not data["next"]:
            break

        urls.append(data["next"])
        url = data["next"]


async def parse_playlist(session, url):
    async with session.get(url) as response:
        data = await response.json()

        with open("ASYNC_RESULT.json", "a") as file:
            result = json.dumps(data["items"], indent=4)
            file.writelines(result)


async def main():
    async with aiohttp.ClientSession(headers=await authenticate()) as session:
        await get_playlist_urls(
            session,
            "https://api.spotify.com/v1/playlists/{}/tracks/".format(PLAYLIST_ID),
        )
        await asyncio.gather(*[parse_playlist(session, url) for url in urls])


if __name__ == "__main__":
    start = perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = perf_counter()
    time = end - start
    print("ASYNC RUN TOOK: {}".format(time))
