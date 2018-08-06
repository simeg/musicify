import unittest

from freezegun import freeze_time

from src.exceptions import SpotifyOAuthError
from src.spotify_oauth import SpotifyOAuth
from .utils import DotNotation, mock_requester, get_exception_msg


def _make_fake_token(expires_at=1531958718, expires_in=1531958718):
    return dict(
        expires_at=expires_at,
        expires_in=expires_in,
        scope="specific-scope",
        token_type="specific-token_type",
        refresh_token="specific-refresh_token",
        access_token="specific-access_token")


def _spotify_oauth(
        requester=None,
        client_id="arbitrary-client_id",
        client_secret="arbitrary-client_secret",
        redirect_uri="arbitrary-redirect_uri",
        state="arbitrary-state",
        scope="arbitrary-scope"
):
    return SpotifyOAuth(
        requester,
        client_id,
        client_secret,
        redirect_uri,
        state,
        scope
    )


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

    # @patch('time.time', mock_time())
    # def test_decorate_with_expires_at(self):
    #     actual = SpotifyOAuth._decorate_with_expires_at(_make_fake_token())
    #     expected = _make_fake_token()
    #     expected['expires_at'] = 3063909918
    #     assert actual == expected

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

    @freeze_time("2012-01-14")
    def test_get_new_token__success(self):
        requester = mock_requester(200, {'specific-key': 'specific-value'})
        sp = _spotify_oauth(requester=requester, state="specific-state")
        actual = sp.get_new_token(
            DotNotation({'args': {'state': 'specific-state',
                                  'code': 'arbitrary-code'}}))
        assert actual == {'expires_in': 10, 'specific-key': 'specific-value',
                          'expires_at': 1326499210}

    def test_get_new_token__failure__when_error(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester)
            _actual = sp.get_new_token(
                DotNotation({'args': {'error': 'arbitrary-value'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "Could not authorize user"

    def test_get_new_token__failure__when_state_mismatch(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester)
            _actual = sp.get_new_token(
                DotNotation({'args': {'state': 'invalid-state-value'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "State mismatch"

    def test_get_new_token__failure__when_no_code(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester, state='specific-state')
            _actual = sp.get_new_token(DotNotation(
                {'args': {'code': None, 'state': 'specific-state'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "Code query param missing"

    @freeze_time("2012-01-14")
    def test_get_new_token__failure_invalid_response(self):
        try:
            requester = mock_requester(400, {}, reason='specific-reason')
            sp = _spotify_oauth(requester=requester, state="specific-state")
            _actual = sp.get_new_token(
                DotNotation({'args': {'state': 'specific-state',
                                      'code': 'arbitrary-code'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "specific-reason"


if __name__ == '__main__':
    unittest.main()
