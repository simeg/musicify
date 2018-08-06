import base64
import logging
import os
import time
from typing import Dict, Union
from urllib.parse import quote

from .exceptions import SpotifyOAuthError

logger = logging.getLogger(__name__)

IS_PRODUCTION = bool(os.environ.get('IS_PRODUCTION', default=False))


class SpotifyOAuth(object):
    """
    Implements Authorization Code Flow for Spotify's OAuth implementation.
    """

    AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    Token = Dict[str, Union[str, int]]
    Headers = Dict[str, str]
    JSONToken = str
    Scope = Union[str, None]

    def __init__(self,
                 requester,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 state: str,
                 scope: str):
        """
            Creates a SpotifyOAuth object
            Parameters:
                 - requester - the object to make HTTP requests
                 - client_id - the client id of your app
                 - client_secret - the client secret of your app
                 - redirect_uri - the redirect URI of your app
                 - state - security state
                 - scope - the desired scope of the request
        """

        self.requester = requester
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state
        self.scope = self._normalize_scope(scope)

    @staticmethod
    def is_token_expired(token: Token) -> bool:
        now = int(time.time())
        return int(token['expires_at']) - now < 60

    @staticmethod
    def json_to_cookie(json: Dict) -> JSONToken:
        return "{}|{}|{}".format(
            json['access_token'],
            json['refresh_token'],
            json['expires_at']
        )

    @staticmethod
    def cookie_to_dict(cookie: str) -> Token:
        split = cookie.split("|")
        return {
            'access_token': split[0],
            'refresh_token': split[1],
            'expires_at': split[2]
        }

    @staticmethod
    def _normalize_scope(scope: str) -> Scope:
        if scope:
            scopes = scope.split(" ")
            scopes.sort()
            return ' '.join(scopes)
        else:
            return None

    @staticmethod
    def _decorate_with_expires_at(token: Token) -> Token:
        """
        Add field to keep track of when
        token expires and should be refreshed
        """
        token['expires_at'] = int(time.time()) + int(token['expires_in'])
        return token

    def get_auth_url(self) -> str:
        return '{}/?' \
               'client_id={}&' \
               'response_type=code&' \
               'redirect_uri={}&' \
               'scope={}&' \
               'state={}' \
            .format(self.AUTHORIZE_URL,
                    self.client_id,
                    quote(self.redirect_uri),
                    self.scope,
                    self.state)

    def get_new_token(self, request) -> Token:
        args = request.args

        if args.get('error') is not None:
            logger.error(
                "Error authorizing user: %s" % str(args.get('error')))
            raise SpotifyOAuthError("Could not authorize user")
        elif args.get('state') != self.state:
            logger.error(
                "Expected state to be: [%s] but was: [%s]" %
                (self.state, str(args.get('state')))
            )
            raise SpotifyOAuthError("State mismatch")
        elif args.get('code') is None:
            raise SpotifyOAuthError("Code query param missing")

        # Request is OK
        code = args.get('code')
        payload = {
            'grant_type': 'authorization_code',
            'code': str(code),
            'redirect_uri': self.redirect_uri,
        }
        response = self.requester.post(self.TOKEN_URL, data=payload,
                                       headers=self._get_headers())

        if response.status_code != 200:
            raise SpotifyOAuthError(response.reason)

        return self._decorate_with_expires_at(response.json())

    def refresh_token(self, token: Token) -> Token:
        refresh_token = token['refresh_token']
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': str(refresh_token)
        }
        response = self.requester.post(self.TOKEN_URL, data=payload,
                                       headers=self._get_headers())

        if response.status_code != 200:
            raise SpotifyOAuthError(response.reason)

        return self._decorate_with_expires_at(response.json())

    def _get_headers(self) -> Headers:
        headers = {
            'Authorization': self._get_auth_header_value(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return headers

    def _get_auth_header_value(self) -> str:
        auth_str = '{}:{}'.format(self.client_id, self.client_secret)
        b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
        return 'Basic {}'.format(b64_auth_str)

    # def legacy_request_auth_token(self) -> Token:
    #     payload = {'grant_type': 'client_credentials'}
    #     headers = {'Authorization': self._get_auth_header_value()}
    #
    #     response = self.requester.post(self.TOKEN_URL, data=payload,
    #                                    headers=headers)
    #     if response.status_code != 200:
    #         raise SpotifyOAuthError(response.reason)
    #
    #     response_data = json.loads(response.text)
    #     access_token = response_data['access_token']
    #
    #     return {'Authorization': 'Bearer {}'.format(access_token)}
