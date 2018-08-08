import logging
from random import randint
from typing import Any, Dict, Set, Union
from flask import abort

from .exceptions import SpotifyClientError
from .emotion_client import Emotions, EmotionClient
from .genres import get_random_genre

logger = logging.getLogger(__name__)

Track = Dict[str, Any]
Tracks = Set[Track]

Uri = Dict[str, str]
Uris = Set[Uri]
Count = int

SpotifyResponse = Dict[str, Any]
SlimResponse = Dict[str, Union[Count, Uri]]

Seed = Dict[str, Union[str, float]]

User = Dict[str, str]


class SpotifyClient(object):
    """
    A wrapper for speaking to the Spotify Web API
    """

    def __init__(self,
                 requester,
                 emotion_client: EmotionClient,
                 token: str):
        """
            Creates a SpotifyClient object
            Parameters:
                 - requester - the object to make HTTP requests
                 - emotion_client - the emotion client instance
                 - token - the Spotify auth token
        """

        self.requester = requester
        self.emotion_client = emotion_client
        self.token = token

    def get_user(self) -> User:
        logger.info("Getting current user profile")

        url = "https://api.spotify.com/v1/me"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % self.token
        }

        response = self.requester.get(url, headers=headers)

        if response.status_code != 200:
            raise SpotifyClientError(response.reason)

        return response.json()

    def _get_uri(self, track: Track) -> Uri:
        return {
            "uri": str(track["uri"])
        }

    def _verify_params(self, emotions: Emotions, limit: int):
        if limit < 1 or limit > 100:
            abort(
                400,
                "The limit param has to be between 1 and 100")  # Bad request
        if not emotions:
            abort(400, "No emotions dict sent")  # Bad request

    def _build_seed(self, emotions: Emotions) -> Seed:
        seed = {
            # Do not include tracks with only spoken word
            "max_speechiness": 0.66,
            # Do not include tracks no one knows about
            "min_popularity": 50,
            "seed_genres": get_random_genre()
        }

        valence_diff = randint(1, 5)

        if self.emotion_client.is_happy(emotions):
            seed["target_mode"] = 1  # Major modality
            seed["target_valence"] = (5 + valence_diff) / 10
        else:
            seed["target_mode"] = 0  # Minor modality
            seed["target_valence"] = (5 - valence_diff) / 10

        return seed

    def _slim_response(self, response: SpotifyResponse) -> SlimResponse:
        """
        Transform Spotify response to slimmed down version
        with exact values that we're interested in.
        """

        tracks = response["tracks"]
        track_uris = list(map(self._get_uri, tracks))
        return {
            "count": int(len(tracks)),
            "uris": track_uris,
        }

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
