import base64
import json
from typing import Dict

import requests
from flask import abort
from urllib.parse import quote

from src import config as cfg
from src.exceptions import SpotifyConnectionError

TEMP_STATE = 'TODO'


def request_auth_token() -> Dict[str, str]:
    url = 'https://accounts.spotify.com/api/token'
    payload = {'grant_type': 'client_credentials'}
    headers = {'Authorization': _auth_header_value()}

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise SpotifyConnectionError(response.reason)

    response_data = json.loads(response.text)
    access_token = response_data['access_token']

    return {'Authorization': 'Bearer {}'.format(access_token)}


def auth_url():
    base_url = 'https://accounts.spotify.com/authorize'
    client_id = cfg.spotify_api()['client_id']
    redirect_uri = quote(
        'http://0.0.0.0:8000/auth-callback')  # TODO: Fix for production
    scope = 'user-read-private'  # TODO: Set correct scope
    state = TEMP_STATE  # TODO: Use localStorage? DB? MemCache?

    return '{}/?client_id={}&response_type=code&redirect_uri={}&scope={}' \
           '&state={}'.format(base_url, client_id, redirect_uri, scope, state)


def get_token(req):
    if req.args.get('error') is not None:
        # TODO: Raise custom exception, do not abort()
        abort(400, 'Found error')
    elif req.args.get('state') != TEMP_STATE:
        # TODO: Raise custom exception, do not abort()
        abort(400, 'State mismatch')
    elif req.args.get('code') is None:
        # TODO: Raise custom exception, do not abort()
        abort(400, 'No code')
    else:
        # Request is OK
        base_url = 'https://accounts.spotify.com/api/token'
        redirect_uri = 'http://0.0.0.0:8000/auth-callback'  # TODO: Fix
        code = req.args.get('code')
        payload = {
            'grant_type': 'authorization_code',
            'code': str(code),
            'redirect_uri': redirect_uri,
        }
        response = requests.post(base_url, data=payload,
                                 headers=_get_headers())

        if response.status_code != 200:
            raise SpotifyConnectionError(
                response.reason)  # TODO: Raise custom exception

        json = response.json()
        # TODO: Store token

        return json  # TODO: Just return what is needed


def refresh_token(refresh_token):
    base_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': str(refresh_token)
    }
    response = requests.post(base_url, data=payload, headers=_get_headers(),
                             verify=True)

    if response.status_code != 200:
        raise SpotifyConnectionError(
            response.reason)  # TODO: Raise custom exception

    return response.json()


def _get_headers():
    headers = {
        'Authorization': _auth_header_value(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return headers


def _auth_header_value():
    config = cfg.spotify_api()
    auth_str = '{}:{}'.format(config['client_id'], config['client_secret'])
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    return 'Basic {}'.format(b64_auth_str)
