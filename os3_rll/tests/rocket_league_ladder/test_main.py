from logging import INFO

from os3_rll.tests import OS3RLLTestCase
from os3_rll.rocket_league_ladder import main


class TestRLLMain(OS3RLLTestCase):
    def setUp(self):
        self.client = self.set_up_patch("os3_rll.rocket_league_ladder.discord_client")
        self.logging = self.set_up_patch("os3_rll.rocket_league_ladder.setup_console_logging")

    def test_main_calls_discord_client(self):
        main()
        self.client.assert_called_once_with()

    def test_main_calls_setup_console_logging(self):
        main()
        self.logging.assert_called_once_with(verbosity=20)
