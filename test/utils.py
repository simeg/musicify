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


def get_exception_msg(exception) -> str:
    return exception.args[0]


class DotNotation(object):
    """
    A class used as a function to pass in dicts to make
    their attributes available using a dot notation
    """

    def __init__(self, _dict):
        self.__dict__ = _dict


def mock_requester(status_code, json, reason=None):
    expires_in_ms = 10

    class MockRequester:
        def __init__(self, _status_code, _json, _reason=None):
            self.status_code = _status_code
            self.json = _json
            self.reason = _reason

        def post(self, *args, **kwargs):
            def __json():
                return {'expires_in': expires_in_ms, **self.json}

            return DotNotation({
                'status_code': self.status_code,
                'json': __json,
                'reason': reason
            })

    return MockRequester(status_code, json)
