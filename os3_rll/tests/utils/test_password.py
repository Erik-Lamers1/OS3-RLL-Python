from string import whitespace

from os3_rll.tests import OS3RLLTestCase
from os3_rll.utils.password import generate_password


class TestPassword(OS3RLLTestCase):
    def test_generate_password_gives_back_the_correct_length(self):
        length = 15
        passwd = generate_password(length)
        self.assertEqual(len(passwd), length)

    def test_generate_password_does_not_include_whitespace(self):
        passwd = generate_password(500)
        for char in whitespace:
            self.assertNotIn(char, passwd)
