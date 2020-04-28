from datetime import datetime, timedelta

from os3_rll.tests import OS3RLLTestCase
from os3_rll.operations.utils import check_date_is_older_than_x_days


class TestCheckDateIsOlderThanXDays(OS3RLLTestCase):
    def setUp(self) -> None:
        self.date = datetime.today()

    def test_check_date_is_older_returns_true_if_date_is_older(self):
        date = self.date - timedelta(days=2)
        self.assertTrue(check_date_is_older_than_x_days(date, 1))

    def test_check_date_is_older_returns_false_if_date_is_not_older(self):
        date = self.date + timedelta(days=2)
        self.assertFalse(check_date_is_older_than_x_days(date, 2))
