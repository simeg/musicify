import logging
from random import randint

import requests

from src.spotify_auth import request_auth_token
from src.emotion_client import is_happy
from src.exceptions import SpotifyConnectionError
from src.genres import get_random_genre

logger = logging.getLogger(__name__)


def get_personalised_tracks(_emotions, limit=1):
    # TODO: Assert limit 1 - 100
    # TODO: Assert _emotions != None ?
    logger.info(
        "Getting [%i] personalised tracks for [%s]" % (limit, _emotions))
    tracks = _get_tracks(_build_seed_entity(_emotions), limit)
    logger.info("Found [%i] personalised tracks " % tracks["count"])
    return tracks


def _get_tracks(seed, limit):
    url = "https://api.spotify.com/v1/recommendations"
    seed["limit"] = limit

    print(seed)

    response = requests.get(url, params=seed, headers=request_auth_token())
    if response.status_code != 200:
        raise SpotifyConnectionError(response.reason)

    return _slim_response(response.json())


def _build_seed_entity(_emotions):
    seed = {
        "max_speechiness": 0.66,  # Do not include tracks with only spoken word
        "min_popularity": 50,  # Do not include tracks no one knows about
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


def _slim_response(spotify_response):
    """Transform Spotify response to slimmed down version
       with exact values that we're interested in"""

    tracks = spotify_response["tracks"]
    slim_tracks = list(map(_get_track, tracks))

    return {
        "count": int(len(tracks)),
        "tracks": slim_tracks,
    }


def _get_track(track):
    return {
        "uri": track["uri"]
    }
