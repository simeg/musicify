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


class SpotifyOAuth(object):
    '''
    Implements Authorization Code Flow for Spotify's OAuth implementation.
    '''

    def __init__(self, client_id, client_secret, redirect_uri, state, scope):
        '''
            Creates a SpotifyOAuth object
            Parameters:
                 - client_id - the client id of your app
                 - client_secret - the client secret of your app
                 - redirect_uri - the redirect URI of your app
                 - state - security state
                 - scope - the desired scope of the request
        '''

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state
        self.scope = self._normalize_scope(scope)

    def auth_url(self):
        base_url = 'https://accounts.spotify.com/authorize'
        client_id = cfg.spotify_api()['client_id']
        redirect_uri = quote(
            'http://0.0.0.0:8000/callback')  # TODO: Fix for production
        scope = 'user-read-private'  # TODO: Set correct scope
        state = TEMP_STATE  # TODO: Use localStorage? DB? MemCache?

        return '{}/?client_id={}&response_type=code&redirect_uri={}&scope={}' \
               '&state={}'.format(base_url, client_id, redirect_uri, scope,
                                  state)

    def request_new_token(self, req):
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
                                     headers=self._get_headers())

            if response.status_code != 200:
                raise SpotifyConnectionError(
                    response.reason)  # TODO: Raise custom exception

            response_json = response.json()
            response_json['expires_at'] = \
                int(time.time()) + response_json['expires_in']

            return response_json

    def refresh_token(self, token):
        refresh_token = token['refresh_token']
        if refresh_token is None:
            abort(400, "Could not find refresh token in token dict")

        base_url = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': str(refresh_token)
        }
        response = requests.post(base_url, data=payload,
                                 headers=self._get_headers())

        if response.status_code != 200:
            raise SpotifyConnectionError(
                response.reason)  # TODO: Raise custom exception

        response_json = response.json()
        response_json['expires_at'] = \
            int(time.time()) + response_json['expires_in']

        return response_json

    def is_token_expired(self, token):
        now = int(time.time())
        return int(token['expires_at']) - now < 60

    def json_to_cookie(self, json):
        return "{}|{}|{}".format(
            json['access_token'],
            json['refresh_token'],
            json['expires_at']
        )

    def cookie_to_dict(self, cookie):
        split = cookie.split("|")
        return {
            'access_token': split[0],
            'refresh_token': split[1],
            'expires_at': split[2]
        }

    def _get_headers(self):
        headers = {
            'Authorization': self._auth_header_value(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return headers

    def _auth_header_value(self):
        config = cfg.spotify_api()
        auth_str = '{}:{}'.format(config['client_id'], config['client_secret'])
        b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
        return 'Basic {}'.format(b64_auth_str)

    def legacy_request_auth_token(self) -> Dict[str, str]:
        url = 'https://accounts.spotify.com/api/token'
        payload = {'grant_type': 'client_credentials'}
        headers = {'Authorization': self._auth_header_value()}

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code != 200:
            raise SpotifyConnectionError(response.reason)

        response_data = json.loads(response.text)
        access_token = response_data['access_token']

        return {'Authorization': 'Bearer {}'.format(access_token)}

    def _normalize_scope(self, scope):
        if scope:
            scopes = scope.split()
            scopes.sort()
            return ' '.join(scopes)
        else:
            return None
