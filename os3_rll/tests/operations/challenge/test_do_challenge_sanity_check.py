from os3_rll.tests import OS3RLLTestCase
from os3_rll.tests.fixture import player_model_fixture
from os3_rll.operations.challenge import do_challenge_sanity_check
from os3_rll.models.challenge import ChallengeException

from datetime import datetime, timedelta


class TestDoChallengeSanityCheck(OS3RLLTestCase):
    def setUp(self) -> None:
        self.p1 = player_model_fixture(rank=10)
        self.p2 = player_model_fixture(_id=2, gamertag="player2", rank=2)

    def test_do_challenge_sanity_check_returns_none_if_all_ok(self):
        self.assertIs(do_challenge_sanity_check(self.p1, self.p2), None)

    def test_do_challenge_sanity_check_raises_challenge_exception_if_p1_is_challenged(self):
        self.p1.challenged = True
        with self.assertRaises(ChallengeException) as e:
            do_challenge_sanity_check(self.p1, self.p2)
        self.assertEqual(e.exception.args[0], "{} is already challenged".format(self.p1.gamertag))

    def test_do_challenge_sanity_check_raises_challenge_exception_if_p2_is_challenged(self):
        self.p2.challenged = True
        with self.assertRaises(ChallengeException) as e:
            do_challenge_sanity_check(self.p1, self.p2)
        self.assertEqual(e.exception.args[0], "{} is already challenged".format(self.p2.gamertag))

    def test_do_challenge_sanity_check_raises_challenge_exception_if_p1_rank_lower_then_p2_rank(self):
        self.p1.rank = 1
        with self.assertRaises(ChallengeException) as e:
            do_challenge_sanity_check(self.p1, self.p2)
        self.assertEqual(e.exception.args[0], "The rank of {} is lower than of {}".format(self.p1.gamertag, self.p2.gamertag))

    def test_do_challenge_sanity_check_raises_challenge_exception_if_player_ranks_are_equal(self):
        self.p1.rank = 2
        with self.assertRaises(ChallengeException) as e:
            do_challenge_sanity_check(self.p1, self.p2)
        self.assertEqual(
            e.exception.args[0],
            "The ranks of both player {} and player {} are the same. This should not happen. "
            "EVERYBODY PANIC!!!".format(self.p1.gamertag, self.p2.gamertag),
        )

    def test_do_challenge_sanity_check_raises_challenge_exception_if_p1_timeout_is_in_the_future(self):
        self.p1.timeout = datetime.now() + timedelta(hours=1)
        with self.assertRaises(ChallengeException) as e:
            do_challenge_sanity_check(self.p1, self.p2)
        self.assertEqual(e.exception.args[0], "The timeout counter of {} is still active".format(self.p1.gamertag))

    def test_do_challenge_sanity_check_does_not_raise_challenge_exception_when_players_are_challenged_and_may_already_be_challenged_passed(
        self,
    ):
        self.p1.challenged = True
        self.p2.challenged = True
        do_challenge_sanity_check(self.p1, self.p2, may_already_by_challenged=True)

    def test_do_challenge_sanity_check_does_not_raise_challenge_exception_when_player1_on_timeout_and_may_be_expired_passed(self):
        self.p1.timeout = datetime.now() + timedelta(days=1)
        do_challenge_sanity_check(self.p1, self.p2, may_be_expired=True)
