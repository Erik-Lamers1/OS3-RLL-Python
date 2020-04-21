from unittest.mock import call, MagicMock

from os3_rll.actions.challenge import create_challenge
from os3_rll.tests import OS3RLLTestCase


class TestCreateChallenge(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.actions.challenge.Player")
        self.challenge = self.set_up_patch("os3_rll.actions.challenge.Challenge", themock=MagicMock)
        self.sanity_check = self.set_up_patch("os3_rll.actions.challenge.do_challenge_sanity_check")

    def test_create_challenge_calls_player_model_with_passed_ids(self):
        p1 = 1
        p2 = 2
        calls = [call(p1), call(p2)]
        create_challenge(p1, p2)
        self.player.assert_has_calls(calls)
