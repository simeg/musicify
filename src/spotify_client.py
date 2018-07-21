import logging
from random import randint
from typing import Any, Dict, Set
from flask import abort

from src.emotion_client import is_happy, Emotions
from src.genres import get_random_genre

logger = logging.getLogger(__name__)


class SpotifyClient(object):
    """
    A wrapper for speaking to the Spotify Web API.
    """

    Track = (str, Any)
    Tracks = Dict[Track]

    Uri = [str, str]
    Uris = Set[Dict[Uri]]
    Count = [str, int]

    SpotifyResponse = Dict[str, Any]
    SlimResponse = Dict[Count, Uris]

    Seed = Dict[str, Any]

    def _slim_response(self, response: SpotifyResponse) -> SlimResponse:
        """
        Transform Spotify response to slimmed down version
        with exact values that we're interested in.
        """

        tracks = response["tracks"]
        track_uris = set(map(self._get_uri, tracks))
        return {
            "count": int(len(tracks)),
            "uris": track_uris,
        }

    def _get_uri(self, track: Track) -> Uri:
        return {
            "uri": track["uri"]
        }

    def _verify_params(self, _emotions: Emotions, limit: int):
        if limit < 1 or limit > 100:
            abort(
                400,
                "The limit param has to be between 1 and 100")  # Bad request
        if not _emotions:
            abort(400, "No emotions dict sent")  # Bad request

    def _build_seed(self, _emotions: Emotions) -> Seed:
        seed = {
            # Do not include tracks with only spoken word
            "max_speechiness": 0.66,
            # Do not include tracks no one knows about
            "min_popularity": 50,
            "seed_genres": get_random_genre()
        }

        valence_diff = randint(1, 5)

        if is_happy(_emotions):
            seed["target_mode"] = 1  # Major modality
            seed["target_valence"] = (5 + valence_diff) / 10
        else:
            seed["target_mode"] = 0  # Minor modality
            seed["target_valence"] = (5 - valence_diff) / 10

        return seed

    # def get_personalised_tracks(
    #         self,
    #         _emotions: Emotions,
    #         limit: int = 1) -> Tracks:
    #     self._verify_params(_emotions, limit)
    #
    #     logger.info(
    #         "Getting [%i] personalised tracks for [%s]" % (limit, _emotions))
    #     tracks = self._get_tracks(self._build_seed_entity(_emotions), limit)
    #     logger.info("Found [%i] personalised tracks " % tracks["count"])
    #     return tracks

    # def _get_tracks(self, seed, limit: int) -> Tracks:
    #     url = "https://api.spotify.com/v1/recommendations"
    #     seed["limit"] = limit
    #
    #     response = requests.get(url, params=seed,
    #                             headers=legacy_request_auth_token())
    #     if response.status_code != 200:
    #         raise SpotifyConnectionError(response.reason)
    #
    #     return self._slim_response(response.json())
