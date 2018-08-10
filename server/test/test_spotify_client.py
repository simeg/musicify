import unittest
import hypothesis.strategies as st
from hypothesis.strategies import text
from hypothesis import given
from werkzeug.exceptions import BadRequest

from src.emotion_client import EmotionClient
from src.spotify_client import SpotifyClient, Track


def _spotify_client(requester=None):
    return SpotifyClient(
        requester,
        EmotionClient(None, "irrelevant-sub-key"),
        "irrelevant-token")


class TestSpotifyOAuth(unittest.TestCase):

    @given(text())
    def test_get_uri(self, value):
        track: Track = {
            "arbitrary-key-1": "arbitrary-value-1",
            "arbitrary-key-2": "arbitrary-value-2",
            "uri": value,
        }
        sp_client = _spotify_client()
        actual = sp_client._get_uri(track)
        expected = {"uri": value}
        assert actual == expected

    @given(st.one_of(st.integers(min_value=100), st.just(0)))
    def test_verify_params__faulty_limit(self, limit):
        try:
            sp_client = _spotify_client()
            sp_client._verify_params({"irrelevant": 0.0}, limit)
        except BadRequest as e:
            assert e.code == 400
            assert e.description == "The limit param has to be between " \
                                    "1 and 100"

    @given(st.integers(min_value=1, max_value=100))
    def test_verify_params__acceptable_limit(self, limit):
        try:
            sp_client = _spotify_client()
            sp_client._verify_params({"irrelevant": 0.0}, limit)
        except BadRequest:
            self.fail("Should not throw exception for limit %s" % limit)

    def test_verify_params__missing_emotions(self):
        try:
            irrelevant_acceptable_limit = 10
            empty_emotions = {}
            sp_client = _spotify_client()
            sp_client._verify_params(
                empty_emotions, irrelevant_acceptable_limit)
        except BadRequest as e:
            assert e.code == 400
            assert e.description == "No emotions dict sent"

    def test_verify_params__acceptable_emotions(self):
        try:
            irrelevant_acceptable_limit = 10
            emotions = {"arbitrary-key": 0.0}
            sp_client = _spotify_client()
            sp_client._verify_params(emotions, irrelevant_acceptable_limit)
        except BadRequest:
            self.fail("Should not throw exception for non-empty emotions")

    def test_build_seed__happy_emotions__major_modality(self):
        emotions = {"happiness": 1, "sadness": 0.9}
        sp_client = _spotify_client()
        seed = sp_client._build_seed(emotions)
        assert seed["target_mode"] == 1

    def test_build_seed__sad_emotions__minor_modality(self):
        emotions = {"happiness": 0.9, "sadness": 1}
        sp_client = _spotify_client()
        seed = sp_client._build_seed(emotions)
        assert seed["target_mode"] == 0

    def test_slim_response(self):
        tracks = []
        for i in range(3):
            tracks.append({
                "arbitrary-key": "arbitrary-value",
                "uri": "key-%s" % str(i)
            })
        full_response = {
            "tracks": tracks
        }
        sp_client = _spotify_client()
        actual = sp_client._slim_response(full_response)
        expected = {
            "count": 3,
            "uris": [
                {"uri": "key-0"},
                {"uri": "key-1"},
                {"uri": "key-2"},
            ]
        }
        assert actual == expected


if __name__ == '__main__':
    unittest.main()
