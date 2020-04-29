from os3_rll.tests import OS3RLLTestCase
from os3_rll.tests.fixture import player_model_fixture, challenge_model_fixture
from os3_rll.actions.challenge import get_challenge


class TestGetChallenge(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.actions.challenge.Player")
        self.player.return_value.get_player_id_by_username.return_value = 10
        self.challenge = self.set_up_patch("os3_rll.actions.challenge.get_latest_challenge_from_player_id")
        self.challenge.return_value = challenge_model_fixture()
        self.player_objs = self.set_up_patch("os3_rll.actions.challenge.get_player_objects_from_challenge_info")
        self.player_objs.return_value = (player_model_fixture(), player_model_fixture(name="Bert"))

    def test_get_challenges_calls_player_model_when_string_is_passed(self):
        get_challenge("blaap")
        self.player.get_player_id_by_username.assert_called_once_with("blaap", discord_name=True)

    def test_get_challenge_calls_player_model_without_searching_for_discord_name(self):
        get_challenge("blaap", search_by_discord_name=False)
        self.player.get_player_id_by_username.assert_called_once_with("blaap", discord_name=False)
