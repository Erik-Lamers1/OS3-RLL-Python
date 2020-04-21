from logging import INFO, DEBUG

from os3_rll.tests import OS3RLLTestCase
from os3_rll.rocket_league_ladder import main


class TestRLLMain(OS3RLLTestCase):
    def setUp(self):
        self.client = self.set_up_patch("os3_rll.rocket_league_ladder.discord_client")
        self.logging = self.set_up_patch("os3_rll.rocket_league_ladder.setup_console_logging")
        self.show_version = self.set_up_patch("os3_rll.rocket_league_ladder.show_version")

    def test_main_calls_discord_client(self):
        main()
        self.client.assert_called_once_with()

    def test_main_calls_setup_console_logging(self):
        main()
        self.logging.assert_called_once_with(verbosity=INFO)

    def test_main_calls_setup_console_logging_verbose(self):
        main(["--verbose"])
        self.logging.assert_called_once_with(verbosity=DEBUG)

    def test_main_calls_show_version_when_version_is_passed(self):
        with self.assertRaises(SystemExit):
            main(["--version"])
        self.show_version.assert_called_once_with()

    def test_main_exits_0_when_version_is_passed(self):
        with self.assertRaises(SystemExit) as e:
            main(["--version"])
        self.assertEqual(e.exception.code, 0)

    def test_main_does_not_call_discord_client_when_version_is_passed(self):
        with self.assertRaises(SystemExit):
            main(["--version"])
        self.client.assert_not_called()
