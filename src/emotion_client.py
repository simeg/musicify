import logging
import operator

import requests

from src import config as cfg
from src.exceptions import EmotionAPIConnectionError, EmotionAPIResponseError

logger = logging.getLogger(__name__)


def get_emotions(image):
    logger.info("Will try to fetch emotions for image")

    url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0' \
          '/detect?returnFaceAttributes=emotion'
    headers = {
        "Content-Type": "application/octet-stream",
        'Ocp-Apim-Subscription-Key': cfg.face_api()['subscription_key'],
    }

    response = requests.post(url, headers=headers, data=image)
    if response.status_code != 200:
        raise EmotionAPIConnectionError(response.reason)

    json = response.json()
    if not json:  # If no face found, an empty array is returned
        raise EmotionAPIResponseError("Could not find a face in the image")

    if len(json) > 1:
        logger.info(
            "Found more than one face in the image, choosing the first one")

    face_emotions = json[0].get('faceAttributes').get('emotion')

    logger.info("Successfully fetched emotions for image")
    return face_emotions


def is_happy(emotions):
    """Slimmed down way of saying if the strongest emotion
       is a happy emotion or not"""
    strongest_emotion = max(emotions.items(), key=operator.itemgetter(1))[0]
    if strongest_emotion == "happiness" or \
            strongest_emotion == "neutral" or \
            strongest_emotion == "surprise":
        return True

    return False
