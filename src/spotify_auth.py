import base64
import json

import requests

from src import config as cfg
from src.exceptions import SpotifyConnectionError


def request_auth_token():
    url = "https://accounts.spotify.com/api/token"
    payload = {'grant_type': 'client_credentials'}

    response = requests.post(url, data=payload, headers=_build_auth_header())
    if response.status_code != 200:
        raise SpotifyConnectionError(response.reason)

    response_data = json.loads(response.text)
    access_token = response_data["access_token"]

    return {"Authorization": "Bearer {}".format(access_token)}


def _build_auth_header():
    config = cfg.spotify_api()
    auth_str = '{}:{}'.format(config['client_id'], config['client_secret'])
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    return {
        'Authorization': 'Basic {}'.format(b64_auth_str)
    }
