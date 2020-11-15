from unittest.mock import call

from os3_rll.tests import OS3RLLTestCase
from os3_rll.actions.challenge_tasks.check_uncompleted_challenges import check_uncompleted_challenges as check_uncompleted


class TestCheckUncompletedChallenges(OS3RLLTestCase):
    def setUp(self) -> None:
        self.db = self.set_up_context_manager_patch("os3_rll.actions.challenge_tasks.check_uncompleted_challenges.Database")
        self.db.return_value.__enter__.return_value.fetchall.return_value = ((0, 1, 2, 3),)
        self.complete = self.set_up_patch("os3_rll.actions.challenge_tasks.check_uncompleted_challenges.complete_challenge")
        self.announce = self.set_up_patch("os3_rll.actions.challenge_tasks.check_uncompleted_challenges.announce_expired_challenge")
        self.announce.return_value = "test_message"
        self.get_challenge = self.set_up_patch("os3_rll.actions.challenge_tasks.check_uncompleted_challenges.get_challenge")
        self.check_date = self.set_up_patch("os3_rll.actions.challenge_tasks.check_uncompleted_challenges.check_date_is_older_than_x_days")
        self.check_date.return_value = True

    def test_check_uncompleted_challenges_makes_correct_db_calls(self):
        calls = [
            call(),
            call().execute("SELECT `id`, `date`, `p1`, `p2` FROM `challenges` WHERE `winner` is NULL"),
            call().fetchall(),
        ]
        check_uncompleted()
        self.db.assert_has_calls(calls)

    def test_check_uncompleted_challenges_checks_date_of_challenge(self):
        check_uncompleted()
        self.check_date.assert_called_once_with(1, 7)

    def test_check_uncompleted_challenges_calls_complete_challenge(self):
        check_uncompleted()
        self.complete.assert_called_once_with(2, 3, "1-0", may_be_expired=True)

    def test_check_uncompleted_challenges_calls_get_challenge(self):
        check_uncompleted()
        self.get_challenge.assert_called_once_with(2, should_be_completed=True)

    def test_check_uncompleted_challenges_calls_announce_expired_challenge(self):
        check_uncompleted()
        self.announce.assert_called_once_with(self.get_challenge())

    def test_check_uncompleted_challenges_puts_announce_message_in_queue(self):
        from os3_rll.discord.queue import discord_message_queue

        check_uncompleted()
        self.assertEqual(discord_message_queue.get(), self.announce.return_value)

    def test_check_uncompleted_challenges_does_not_call_complete_challenge_methods_when_check_date_returns_false(self):
        self.check_date.return_value = False
        check_uncompleted()
        self.assertFalse(self.complete.called)
        self.assertFalse(self.announce.called)
        self.assertFalse(self.get_challenge.called)

    def test_check_uncompleted_challenges_loops_over_the_db_return_values(self):
        self.db.return_value.__enter__.return_value.fetchall.return_value = ((0, 1, 2, 3), (4, 5, 6, 7))
        calls = [call(2, 3, "1-0", may_be_expired=True), call(6, 7, "1-0", may_be_expired=True)]
        check_uncompleted()
        self.complete.assert_has_calls(calls)
