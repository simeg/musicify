import logging
import operator
from typing import Dict

from .exceptions import EmotionClientError

logger = logging.getLogger(__name__)

Emotions = Dict[str, float]


class EmotionClient(object):
    """
    A wrapper for speaking to the Microsoft Face Cognitive API.
    """

    EMOTIONS_API_URL = 'https://northeurope.api.cognitive.microsoft.com/' \
                       'face/v1.0/detect?returnFaceAttributes=emotion'

    def __init__(self, requester, subscription_key: str):
        """
            Creates a EmotionClient object
            Parameters:
                 - subscription_key - the subscription key to the API
        """

        self.requester = requester
        self.subscription_key = subscription_key

    @staticmethod
    def is_happy(emotions: Emotions) -> bool:
        """
        Trivial way of saying if the strongest
        emotion is a happy emotion or not
        """
        strongest_emotion = max(emotions.items(),
                                key=operator.itemgetter(1))[0]
        if strongest_emotion == "happiness" or \
                strongest_emotion == "neutral" or \
                strongest_emotion == "surprise":
            return True

        return False

    def get_emotions(self, image) -> Emotions:
        if image is None:
            logger.error("Image is missing")
            raise EmotionClientError("Image is missing")

        headers = {
            "Content-Type": "application/octet-stream",
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }

        logger.info("Fetching emotions for image")

        response = self.requester.post(self.EMOTIONS_API_URL, headers=headers,
                                       data=image)

        if response.status_code != 200:
            raise EmotionClientError(response.reason)

        json = response.json()
        if not json:  # If no face found, an empty array is returned
            raise EmotionClientError("Could not find a face in the image")

        if len(json) > 1:
            logger.warning(
                "Found more than one face in the image,"
                " choosing the first one")

        face_emotions = json[0].get('faceAttributes').get('emotion')

        logger.info("Successfully fetched emotions for image")
        return face_emotions
