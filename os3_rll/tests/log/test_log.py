import logging

from os3_rll.log.log import setup_console_logging
from os3_rll.tests import TestCase
from os3_rll.conf import settings


class TestLog(TestCase):
    def test_setup_console_logging_sets_up_INFO_logging_by_default(self):
        setup_console_logging()
        self.assertEqual(settings.LOGGING['handlers']['console']['level'], logging.INFO)

    def test_setup_console_logging_sets_up_passed_logging_level(self):
        setup_console_logging(logging.DEBUG)
        self.assertEqual(settings.LOGGING['handlers']['console']['level'], logging.DEBUG)
