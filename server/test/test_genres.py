import unittest

from src.genres import get_genres, get_random_genre


class TestGenres(unittest.TestCase):

    def test_get_random_genre(self):
        assert get_random_genre()
        assert isinstance(get_random_genre(), str)

    def test_get_genres(self):
        assert len(get_genres()) == 126


if __name__ == '__main__':
    unittest.main()
