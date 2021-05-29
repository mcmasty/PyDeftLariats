from unittest import TestCase
from hamcrest import assert_that, equal_to


class TestAnythingMatcher(TestCase):
    def test_is_match(self):
        assert_that(True, equal_to(True), "Dumb test.")
