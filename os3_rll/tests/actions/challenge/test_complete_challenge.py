from unittest.mock import call, MagicMock, ANY

from os3_rll.actions.challenge import complete_challenge
from os3_rll.models.challenge import ChallengeException
from os3_rll.tests import OS3RLLTestCase


class TestCompleteChallenge(OS3RLLTestCase):
    def setUp(self) -> None:
        self.p1 = 1
        self.p2 = 2
        self.player = self.set_up_patch("os3_rll.actions.challenge.Player", themock=MagicMock())
        self.player.return_value.__enter__.return_value.id = self.p1
        self.challenge = self.set_up_patch("os3_rll.actions.challenge.Challenge", themock=MagicMock())
        self.challenge.return_value.__enter__.return_value.winner = self.p1
        self.sanity_check = self.set_up_patch("os3_rll.actions.challenge.do_challenge_sanity_check")
        self.process_completed_challenges_args = self.set_up_patch("os3_rll.actions.challenge.process_completed_challenge_args")
        self.process_completed_challenges_args.return_value = (1, 0, 2, 1)
        self.check_date_older_then = self.set_up_patch("os3_rll.actions.challenge.check_date_is_older_than_x_days")
        self.check_date_older_then.return_value = False

    def test_complete_challenge_calls_player_model_with_passed_ids(self):
        calls = [call(self.p1), ANY, call(self.p2)]
        complete_challenge(self.p1, self.p2, "blaap")
        self.player.assert_has_calls(calls)

    def test_complete_challenge_calls_player_model_with_discord_name(self):
        p1 = "blaap#123"
        p2 = "blaap#456"
        calls = [call.get_player_id_by_username(p1, discord_name=True), call.get_player_id_by_username(p2, discord_name=True)]
        complete_challenge(p1, p2, "blaap")
        self.player.assert_has_calls(calls)

    def test_complete_challenge_calls_process_completed_challenge_args(self):
        complete_challenge(self.p1, self.p2, "blaap")
        self.process_completed_challenges_args.assert_called_once_with("blaap")

    def test_complete_challenge_calls_get_latest_challenge_from_player(self):
        complete_challenge(self.p1, self.p2, "blaap")
        self.challenge.get_latest_challenge_from_player.assert_called_once_with(self.p1, self.p1)

    def test_complete_challenge_calls_sanity_check(self):
        complete_challenge(self.p1, self.p2, "blaap")
        self.sanity_check.assert_called_once_with(
            self.player().__enter__(), self.player().__enter__(), may_already_by_challenged=True, may_be_expired=False
        )

    def test_complete_challenge_calls_sanity_check_when_passing_may_be_expired(self):
        complete_challenge(self.p1, self.p2, "blaap", may_be_expired=True)
        self.sanity_check.assert_called_once_with(
            self.player().__enter__(), self.player().__enter__(), may_already_by_challenged=True, may_be_expired=True
        )

    def test_complete_challenge_calls_check_date_older_then(self):
        complete_challenge(self.p1, self.p2, "blaap")
        self.check_date_older_then.assert_called_once_with(self.challenge().__enter__().date, 7)

    def test_complete_challenge_raises_challenge_exception(self):
        self.check_date_older_then.return_value = True
        with self.assertRaises(ChallengeException):
            complete_challenge(self.p1, self.p2, "blaap")

    def test_complete_challenge_does_not_raise_challenge_exception_when_passing_may_be_expired(self):
        self.check_date_older_then.return_value = True
        complete_challenge(self.p1, self.p2, "blaap", may_be_expired=True)

    def test_complete_challenge_raises_challenge_exception_when_unknown_winner(self):
        self.challenge.return_value.__enter__.return_value.winner = None
        with self.assertRaises(ChallengeException):
            complete_challenge(self.p1, self.p2, "blaap")

    def test_complete_challenge_calls_player_sql_query(self):
        complete_challenge(self.p1, self.p2, "blaap")
        self.player().__enter__().db.execute.assert_called_once()

    def test_complete_challenge_calls_save_on_challenge_model(self):
        complete_challenge(self.p1, self.p2, "blaap")
        self.challenge().__enter__().save.assert_called_once_with()

    def test_complete_challenge_saves_both_player_models(self):
        complete_challenge(self.p1, self.p2, "blaap")
        calls = [call().__enter__().save(), call().__enter__().save()]
        self.player.assert_has_calls(calls)

    def test_complete_challenge_returns_the_id_set_according_to_the_challenge_model_winner(self):
        self.assertEqual(complete_challenge(self.p1, self.p2, "blaap"), self.p1)
