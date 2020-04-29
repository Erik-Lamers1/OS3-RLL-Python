from unittest.mock import call

from os3_rll.tests import OS3RLLTestCase
from os3_rll.tests.fixture import player_model_fixture
from os3_rll.actions.player import reset_player_password


class TestAddPlayer(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.actions.player.Player")
        self.player.return_value = player_model_fixture()
        self.gen_passwd = self.set_up_patch("os3_rll.actions.player.generate_password")
        self.gen_passwd.return_value = "password"

    def test_reset_player_password_calls_player_model(self):
        reset_player_password("jaap")
        self.player.assert_called_once_with(self.player.get_player_id_by_username())
        calls = [call("jaap", discord_name=False), call()]
        self.player.get_player_id_by_username.assert_has_calls(calls)

    def test_reset_player_password_calls_player_model_with_discord_name(self):
        reset_player_password("jaap", discord_name=True)
        self.player.assert_called_once_with(self.player.get_player_id_by_username())
        calls = [call("jaap", discord_name=True), call()]
        self.player.get_player_id_by_username.assert_has_calls(calls)

    def test_reset_player_password_calls_generate_password(self):
        reset_player_password("jaap")
        self.gen_passwd.assert_called_once_with()

    def test_reset_player_password_returns_generated_password(self):
        self.assertEqual(reset_player_password("jaap"), self.gen_passwd.return_value)
