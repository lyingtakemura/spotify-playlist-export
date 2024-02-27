import asyncio
import json
import logging
import os
from base64 import b64encode
from time import perf_counter

import httpx
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_access_token() -> dict:
    """
    - encode client_id and client_secret to base64 string
    - request spotify api access_token by base64 string
    """
    b64string = b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "utf-8"))
    b64string = b64string.decode("utf-8")

    headers = {"Authorization": f"Basic {b64string}"}
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}

    response = httpx.post(url=url, data=data, headers=headers).json()["access_token"]

    return {
        "Authorization": f"Bearer {response}",
        "grant_type": "access_token",
    }


urls = []
playlist_id = os.getenv("PLAYLIST_ID")
client = httpx.AsyncClient(headers=get_access_token())


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
