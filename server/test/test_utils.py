import unittest
import hypothesis.strategies as st
from hypothesis import given, settings

import utils
from utils import allowed_file_type, exists
from server.test.utils import one_of_all_primitives


class TestUtils(unittest.TestCase):

    @given(st.sampled_from(sorted(utils.ALLOWED_IMAGE_EXTENSIONS)), st.text())
    def test_allowed_file_type__pass(self, extension, name):
        file_name = "{}.{}".format(name, extension)
        assert allowed_file_type(file_name)
        assert allowed_file_type('blob')

    @given(st.sampled_from(sorted(["unsupported"])), st.text())
    @settings(max_examples=1)
    def test_allowed_file_type__fail(self, extension, name):
        file_name = "{}.{}".format(name, extension)
        assert allowed_file_type(file_name) is False

    @given(st.one_of(one_of_all_primitives()))
    def test_exists__pass(self, value):
        assert exists(value)

    @given(st.none())
    @settings(max_examples=1)
    def test_exists__fail(self, value):
        assert exists(value) is False


if __name__ == '__main__':
    unittest.main()
