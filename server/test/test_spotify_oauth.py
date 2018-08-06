import unittest

from freezegun import freeze_time

from src.exceptions import SpotifyOAuthError
from src.spotify_oauth import SpotifyOAuth, Token
from .utils import DotNotation, mock_requester, get_exception_msg


def _fake_token(expires_at=1531958718,
                expires_in=1531958718,
                scope="specific-scope",
                token_type="specific-token_type",
                refresh_token="specific-refresh_token",
                access_token="specific-access_token") -> Token:
    return dict(
        expires_at=expires_at,
        expires_in=expires_in,
        scope=scope,
        token_type=token_type,
        refresh_token=refresh_token,
        access_token=access_token)


def _spotify_oauth(
        requester=None,
        client_id="arbitrary-client_id",
        client_secret="arbitrary-client_secret",
        redirect_uri="arbitrary-redirect_uri",
        state="arbitrary-state",
        scope="arbitrary-scope"
) -> SpotifyOAuth:
    return SpotifyOAuth(
        requester,
        client_id,
        client_secret,
        redirect_uri,
        state,
        scope
    )


class TestSpotifyOAuth(unittest.TestCase):

    @freeze_time("2012-01-14 12:00:00")
    def test_is_token_expired__pass(self):
        now = 1326542400
        expired_token = {
            'expires_at': now,
        }
        result = SpotifyOAuth.is_token_expired(expired_token)
        assert result

    @freeze_time("2012-01-14 12:00:00")
    def test_is_token_expired__fail(self):
        now = 1326542400
        not_expired_token = {
            'expires_at': (now + 61),
        }
        result = SpotifyOAuth.is_token_expired(not_expired_token)
        assert not result

    def test_json_to_cookie(self):
        actual = SpotifyOAuth.json_to_cookie(_fake_token())
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

    @freeze_time("2012-01-14 12:00:00")
    def test_decorate_with_expires_at(self):
        now = 1326542400
        token = {
            'expires_in': 1
        }
        result = SpotifyOAuth._decorate_with_expires_at(token)
        assert result['expires_at'] == (now + 1)

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
        expected = {'expires_in': 10, 'specific-key': 'specific-value',
                    'expires_at': 1326499210}
        assert actual == expected

    def test_get_new_token__failure__when_error(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester)
            _ = sp.get_new_token(
                DotNotation({'args': {'error': 'arbitrary-value'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "Could not authorize user"

    def test_get_new_token__failure__when_state_mismatch(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester)
            _ = sp.get_new_token(
                DotNotation({'args': {'state': 'invalid-state-value'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "State mismatch"

    def test_get_new_token__failure__when_no_code(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester, state='specific-state')
            _ = sp.get_new_token(DotNotation(
                {'args': {'code': None, 'state': 'specific-state'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "Code query param missing"

    @freeze_time("2012-01-14")
    def test_get_new_token__failure__when_invalid_response(self):
        try:
            requester = mock_requester(400, {}, reason='specific-reason')
            sp = _spotify_oauth(requester=requester, state="specific-state")
            _ = sp.get_new_token(
                DotNotation({'args': {'state': 'specific-state',
                                      'code': 'arbitrary-code'}}))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "specific-reason"

    @freeze_time("2012-01-14 12:00:00")
    def test_refresh_token__success(self):
        requester = mock_requester(200, {'expires_in': 1})
        sp = _spotify_oauth(requester=requester)
        actual = sp.refresh_token(_fake_token(expires_in=1))
        expected = {'expires_in': 1, 'expires_at': 1326542401}
        assert actual == expected

    def test_refresh_token__failure__when_no_refresh_token(self):
        try:
            requester = mock_requester(500, {})
            sp = _spotify_oauth(requester=requester)
            _ = sp.refresh_token(_fake_token(refresh_token=None))
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "Invalid token"

    def test_refresh_token__failure__when_invalid_response(self):
        try:
            requester = mock_requester(400, {}, reason='specific-reason')
            sp = _spotify_oauth(requester=requester)
            _ = sp.refresh_token(_fake_token())
        except SpotifyOAuthError as e:
            assert e is not None
            assert get_exception_msg(e) == "specific-reason"


if __name__ == '__main__':
    unittest.main()
