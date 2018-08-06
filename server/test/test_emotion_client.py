import unittest

from src.emotion_client import EmotionClient


class TestEmotionClient(unittest.TestCase):

    def test_is_happy__true(self):
        e_client = EmotionClient("irrelevant-sub-key")
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
