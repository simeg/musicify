import unittest

from src.emotion_client import EmotionClient


def _emotion_client(requester=None) -> EmotionClient:
    return EmotionClient(requester, "irrelevant-sub-key")


class TestEmotionClient(unittest.TestCase):

    def test_is_happy__true(self):
        e_client = _emotion_client()
        emotions = {
            "happiness": 1,
            "neutral": 0.5,
            "surprise": 0.5,
            "sadness": 0.5,
        }
        assert e_client.is_happy(emotions)
        emotions = {
            "happiness": 0.5,
            "neutral": 1,
            "surprise": 0.5,
            "sadness": 0.5,
        }
        assert e_client.is_happy(emotions)
        emotions = {
            "happiness": 0.5,
            "neutral": 0.5,
            "surprise": 1,
            "sadness": 0.5,
        }
        assert e_client.is_happy(emotions)


if __name__ == '__main__':
    unittest.main()
