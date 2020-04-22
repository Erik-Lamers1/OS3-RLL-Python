from unittest.mock import call, MagicMock, ANY

from os3_rll.actions.challenge import reset_challenge
from os3_rll.models.challenge import ChallengeException
from os3_rll.tests import OS3RLLTestCase


class TestResetChallenge(OS3RLLTestCase):
    def setUp(self) -> None:
        self.p1 = 1
        self.p2 = 2
        self.player = self.set_up_patch("os3_rll.actions.challenge.Player", themock=MagicMock())
        self.player.return_value.__enter__.return_value.id = self.p1
        self.player.return_value.__enter__.return_value.challenged = False
        self.player.return_value.__enter__.return_value.rank = 1
        self.challenge = self.set_up_patch("os3_rll.actions.challenge.Challenge", themock=MagicMock())
        self.challenge.return_value.__enter__.return_value.winner = self.p1
        self.sanity_check = self.set_up_patch("os3_rll.actions.challenge.do_challenge_sanity_check")
        self.check_date_older_then = self.set_up_patch("os3_rll.actions.challenge.check_date_is_older_than_x_days")
        self.check_date_older_then.return_value = False

    def test_reset_challenge_calls_player_model_with_passed_ids(self):
        calls = [call(self.p1), ANY, call(self.p2)]
        reset_challenge(self.p1, self.p2)
        self.player.assert_has_calls(calls)

    def test_reset_challenge_calls_player_model_with_discord_name(self):
        p1 = "blaap#123"
        p2 = "blaap#456"
        calls = [call.get_player_id_by_username(p1, discord_name=True), call.get_player_id_by_username(p2, discord_name=True)]
        reset_challenge(p1, p2)
        self.player.assert_has_calls(calls)

    def test_reset_challenge_raises_challenge_exception_when_player_is_already_challenged(self):
        self.player.return_value.__enter__.return_value.challenged = True
        with self.assertRaises(ChallengeException):
            reset_challenge(self.p1, self.p2)

    def test_reset_challenge_calls_get_latest_challenge_from_player(self):
        reset_challenge(self.p1, self.p2)
        self.challenge.get_latest_challenge_from_player.assert_called_once_with(self.p1, self.p1, should_be_completed=True)

    def test_reset_challenge_calls_check_date_older_then(self):
        reset_challenge(self.p1, self.p2)
        self.check_date_older_then.assert_called_once_with(self.challenge().__enter__().date, 7)

    def test_reset_challenge_raises_challenge_exception_when_challenge_expired(self):
        self.check_date_older_then.return_value = True
        with self.assertRaises(ChallengeException):
            reset_challenge(self.p1, self.p2)

    def test_reset_challenge_raises_challenge_exception_when_unknown_winner(self):
        self.challenge.return_value.__enter__.return_value.winner = None
        with self.assertRaises(ChallengeException):
            reset_challenge(self.p1, self.p2)

    def test_reset_challenge_calls_challenge_model_reset_function(self):
        reset_challenge(self.p1, self.p2)
        self.challenge().__enter__().reset.assert_called_once_with()

    def test_reset_challenge_saves_both_player_models(self):
        reset_challenge(self.p1, self.p2)
        calls = [call().__enter__().save(), call().__enter__().save()]
        self.player.assert_has_calls(calls)
