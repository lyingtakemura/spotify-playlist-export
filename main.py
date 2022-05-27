import os
from base64 import b64encode

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

b64string = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode("ASCII")
b64string = b64encode(b64string)
b64string = bytes.decode(b64string)

url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": "Basic {}".format(b64string)
}
data = {
    "grant_type": "client_credentials"
}

response = requests.post(url, headers=headers, data=data)

print(response.text)
