from os3_rll.tests import TestCase
from os3_rll.utils.math import ordinal


class TestMath(TestCase):
    def test_ordinal_returns_first(self):
        self.assertEqual(ordinal(1), '1st')

    def test_ordinal_returns_second(self):
        self.assertEqual(ordinal(2), '2nd')

    def test_ordinal_returns_third(self):
        self.assertEqual(ordinal(3), '3rd')

    def test_ordinal_returns_fourth(self):
        self.assertEqual(ordinal(4), '4th')

    def test_ordinal_returns_twenty_second(self):
        self.assertEqual(ordinal(22), '22nd')

    def test_ordinal_returns_one_hunderd_and_first(self):
        self.assertEqual(ordinal(101), '101st')
