import time
from datetime import datetime
from unittest.mock import Mock

import hypothesis.strategies as st


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


class dot_notiation(object):
    """
    A class used as a function to pass in dicts to make
    their attributes available using a dot notation
    """

    def __init__(self, d):
        self.__dict__ = d
