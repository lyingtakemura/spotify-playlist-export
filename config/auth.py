import os
from base64 import b64encode

import httpx
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_headers() -> dict:
    """
    - encode client_id and client_secret to base64 string
    - request spotify api access_token by base64 string
    """
    try:
        b64string = b64encode(bytes(f"{client_id}:{client_secret}", "utf-8"))
        b64string = b64string.decode("utf-8")

        headers = {"Authorization": f"Basic {b64string}"}
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}

        response = httpx.post(url=url, data=data, headers=headers)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Error {e.response.status_code} while requesting {e.request.url}")

        token = response.json().get("access_token")
        if token == None:
            raise Exception("No token in response")

        return {
            "Authorization": f"Bearer {token}",
            "grant_type": "access_token",
        }
    except Exception as e:
        print(e)


if __name__ == "__main__":
    get_headers()
