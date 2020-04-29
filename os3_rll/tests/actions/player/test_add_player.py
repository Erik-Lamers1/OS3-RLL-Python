from unittest.mock import call

from os3_rll.tests import OS3RLLTestCase
from os3_rll.tests.fixture import player_model_fixture
from os3_rll.actions.player import add_player


class TestAddPlayer(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.actions.player.Player")
        self.player.return_value = player_model_fixture()
        self.gen_passwd = self.set_up_patch("os3_rll.actions.player.generate_password")
        self.gen_passwd.return_value = "password"

    def test_add_player_calls_player_model(self):
        add_player("henk", "henk123", "henk456")
        calls = [call(), call.get_player_id_by_username("henk123")]
        self.player.assert_has_calls(calls)

    def test_add_player_call_generate_password_method(self):
        add_player("henk", "henk123", "henk345")
        self.gen_passwd.assert_called_once_with()

    def test_add_player_sets_correct_values(self):
        add_player("henk", "henk123", "henk456")
        self.assertEqual(self.player.return_value.name, "henk")
        self.assertEqual(self.player.return_value.gamertag, "henk123")
        self.assertEqual(self.player.return_value.discord, "henk456")
