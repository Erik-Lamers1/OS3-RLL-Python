from unittest.mock import call, MagicMock, PropertyMock, Mock

from os3_rll.actions.challenge import create_challenge
from os3_rll.tests import OS3RLLTestCase


class TestCreateChallenge(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.actions.challenge.Player")
        self.challenge = self.set_up_patch("os3_rll.actions.challenge.Challenge", themock=MagicMock())
        self.sanity_check = self.set_up_patch("os3_rll.actions.challenge.do_challenge_sanity_check")

    def test_create_challenge_calls_player_model_with_passed_ids(self):
        p1 = 1
        p2 = 2
        calls = [call(p1), call(p2)]
        create_challenge(p1, p2)
        self.player.assert_has_calls(calls)

    def test_create_challenge_calls_player_model_with_discord_name(self):
        p1 = "blaap#123"
        p2 = "blaap#456"
        calls = [call.get_player_id_by_username(p1, discord_name=True), call.get_player_id_by_username(p2, discord_name=True)]
        create_challenge(p1, p2)
        self.player.assert_has_calls(calls)

    def test_create_challenge_calls_player_model_with_gamertag(self):
        p1 = "blaap#123"
        p2 = "blaap#456"
        calls = [call.get_player_id_by_username(p1, discord_name=False), call.get_player_id_by_username(p2, discord_name=False)]
        create_challenge(p1, p2, search_by_discord_name=False)
        self.player.assert_has_calls(calls)

    def test_create_challenge_calls_sanity_check(self):
        create_challenge(1, 2)
        self.sanity_check.assert_called_once_with(self.player(), self.player())

    def test_create_challenge_calls_challenge_model(self):
        create_challenge(1, 2)
        self.challenge.assert_called_once_with()

    def test_create_challenge_saves_both_player_models(self):
        calls = [call().save()] * 2
        create_challenge(1, 2)
        self.player.assert_has_calls(calls)
