import time
import hypothesis.strategies as st

from datetime import datetime
from unittest.mock import Mock


def one_of_all_primitives(additional_type=None):
    if additional_type:
        return st.one_of(
            st.integers(),
            st.floats(),
            st.text(),
            st.booleans(),
            additional_type())

    return st.one_of(
        st.integers(),
        st.floats(),
        st.text(),
        st.booleans())


def mock_time():
    mock = Mock()
    mock.return_value = time.mktime(datetime(2018, 7, 19).timetuple())
    return mock


class DotNotation(object):
    """
    A class used as a function to pass in dicts to make
    their attributes available using a dot notation
    """

    def __init__(self, _dict):
        self.__dict__ = _dict


def mock_requester(status_code, json):
    class MockRequester:
        def __init__(self, _status_code, _json):
            self.status_code = _status_code
            self.json = _json

        def post(self, *args, **kwargs):
            def __json():
                return {'expires_in': 10, **self.json}

            return DotNotation({
                'status_code': self.status_code,
                'json': __json
            })

    return MockRequester(status_code, json)
