import base64
import json
import logging
import os
import time
from typing import Dict

import requests
from flask import abort
from urllib.parse import quote

from src import config as cfg
from src.exceptions import SpotifyConnectionError

logger = logging.getLogger(__name__)

IS_PRODUCTION = bool(os.environ.get('IS_PRODUCTION', default=False))

TEMP_STATE = 'TODO'
FILE_PATH_TOKEN = "/tmp/spotify_token"


def auth_url():
    base_url = 'https://accounts.spotify.com/authorize'
    client_id = cfg.spotify_api()['client_id']
    redirect_uri = quote(
        'http://0.0.0.0:8000/callback')  # TODO: Fix for production
    scope = 'user-read-private'  # TODO: Set correct scope
    state = TEMP_STATE  # TODO: Use localStorage? DB? MemCache?

    return '{}/?client_id={}&response_type=code&redirect_uri={}&scope={}' \
           '&state={}'.format(base_url, client_id, redirect_uri, scope, state)


def request_token(req):
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
        redirect_uri = 'http://0.0.0.0:8000/callback'  # TODO: Fix
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
        json['expires_at'] = int(time.time()) + json['expires_in']
        cache_token(json)

        return json  # TODO: Just return what is needed


def get_token():
    try:
        return _read_cached_token()
    except IOError:
        return None


def refresh_token(token):
    refresh_token = token['refresh_token']
    if refresh_token is None:
        abort(400, "Could not find refresh token in token dict")

    base_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': str(refresh_token)
    }
    response = requests.post(base_url, data=payload, headers=_get_headers())

    if response.status_code != 200:
        raise SpotifyConnectionError(
            response.reason)  # TODO: Raise custom exception

    return response.json()


def cache_token(token_info):
    try:
        f = open(FILE_PATH_TOKEN, 'w')
        f.write(json.dumps(token_info))
        f.close()
        logger.info("Successfully wrote token to cache")
    except IOError:
        logger.error("Unable to write token cache to [%s]" % FILE_PATH_TOKEN)
        pass


def _read_cached_token():
    try:
        f = open(FILE_PATH_TOKEN, 'r')
        token_info = f.read()
        f.close()
        return json.loads(token_info)
    except IOError:
        logger.error("Unable to read from file at [%s]" % FILE_PATH_TOKEN)
        return None


def is_token_expired(token):
    now = int(time.time())
    token_is_expired = token['expires_at'] - now < 60
    logger.info("Token is expired is [%s]" % token_is_expired)
    return token_is_expired


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


def legacy_request_auth_token() -> Dict[str, str]:
    url = 'https://accounts.spotify.com/api/token'
    payload = {'grant_type': 'client_credentials'}
    headers = {'Authorization': _auth_header_value()}

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise SpotifyConnectionError(response.reason)

    response_data = json.loads(response.text)
    access_token = response_data['access_token']

    return {'Authorization': 'Bearer {}'.format(access_token)}
