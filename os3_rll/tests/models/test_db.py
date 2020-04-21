from os3_rll.tests import OS3RLLTestCase
from os3_rll.models.db import Database
from os3_rll.conf import settings


class TestDBModel(OS3RLLTestCase):
    def setUp(self) -> None:
        self.connect = self.set_up_patch("os3_rll.models.db.connect")

    def test_db_connect_calls_connect_method(self):
        Database()
        self.connect.assert_called_once_with(settings.DB_HOST, settings.DB_USER, settings.DB_PASS, settings.DB_DATABASE)
