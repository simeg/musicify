import unittest
from unittest.mock import patch

from src.spotify_oauth import SpotifyOAuth
from test.utils import mock_time


def _make_fake_token(expires_at=1531958718, expires_in=1531958718):
    return dict(
        expires_at=expires_at,
        expires_in=expires_in,
        scope="specific-scope",
        token_type="specific-token_type",
        refresh_token="specific-refresh_token",
        access_token="specific-access_token")


def _spotify_oauth(
        client_id="arbitrary-client_id",
        client_secret="arbitrary-client_secret",
        redirect_uri="arbitrary-redirect_uri",
        state="arbitrary-state",
        scope="arbitrary-scope"
):
    return SpotifyOAuth(client_id, client_secret, redirect_uri, state, scope)


class TestSpotifyOAuth(unittest.TestCase):

    def test_json_to_cookie(self):
        actual = SpotifyOAuth.json_to_cookie(_make_fake_token())
        expected = "specific-access_token|specific-refresh_token|1531958718"
        assert actual == expected

    def test_cookie_to_dict(self):
        cookie = "specific-access_token|specific-refresh_token|1531958718"
        actual = SpotifyOAuth.cookie_to_dict(cookie)
        expected = {
            "access_token": "specific-access_token",
            "refresh_token": "specific-refresh_token",
            "expires_at": "1531958718",
        }
        assert actual == expected

    def test_normalize_scope__pass(self):
        scope = "specific-scope-3 specific-scope-2 specific-scope-1"
        actual = SpotifyOAuth._normalize_scope(scope)
        expected = "specific-scope-1 specific-scope-2 specific-scope-3"
        assert actual == expected

    def test_normalize_scope__fail(self):
        scope = ""
        actual = SpotifyOAuth._normalize_scope(scope)
        expected = None
        assert actual == expected

    @patch('time.time', mock_time())
    def test_decorate_with_expires_at(self):
        actual = SpotifyOAuth._decorate_with_expires_at(_make_fake_token())
        expected = _make_fake_token()
        expected['expires_at'] = 3063909918
        assert actual == expected

    def test_get_auth_url(self):
        sp_oauth = _spotify_oauth(
            client_id="specific-client_id",
            redirect_uri="specific-redirect_uri",
            state="specific-state",
            scope="specific-scope",
        )
        actual = sp_oauth.get_auth_url()
        expected = "https://accounts.spotify.com/authorize/?" \
                   "client_id=specific-client_id&response_type=code&" \
                   "redirect_uri=specific-redirect_uri&scope=specific-scope&" \
                   "state=specific-state"
        assert actual == expected

    def test_get_auth_header_value(self):
        sp_oauth = _spotify_oauth(
            client_id="specific-client_id",
            client_secret="specific-client_secret"
        )
        actual = sp_oauth._get_auth_header_value()
        expected = "Basic " \
                   "c3BlY2lmaWMtY2xpZW50X2lkOnNwZWNpZmljLWNsaWVudF9zZWNyZXQ="
        assert actual == expected

    def test_get_headers(self):
        sp_oauth = _spotify_oauth(
            client_id="specific-client_id",
            client_secret="specific-client_secret"
        )
        actual = sp_oauth._get_headers()
        expected = {
            'Authorization': sp_oauth._get_auth_header_value(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        assert actual == expected


if __name__ == '__main__':
    unittest.main()
