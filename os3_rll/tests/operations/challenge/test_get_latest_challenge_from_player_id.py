from unittest.mock import call, Mock

from os3_rll.tests import OS3RLLTestCase
from os3_rll.tests.fixture import player_model_fixture
from os3_rll.operations.challenge import get_latest_challenge_from_player_id
from os3_rll.models.player import PlayerException


class TestGetLatestChallengeFromPlayerId(OS3RLLTestCase):
    def setUp(self) -> None:
        self.db = Mock()
        self.player = self.set_up_context_manager_patch("os3_rll.operations.challenge.Player")
        self.player_model = player_model_fixture(db_mock=self.db, challenged=True)
        self.player.return_value.__enter__.return_value = self.player_model
        self.db.rowcount = 1
        self.db.fetchone.return_value = (10,)
        self.challenge = self.set_up_patch("os3_rll.operations.challenge.Challenge")
        self.challenge.return_value = 42

    def test_get_latest_challenge_from_player_id_calls_player_model(self):
        get_latest_challenge_from_player_id(1)
        self.player.assert_called_once_with(1)

    def test_get_latest_challenge_from_player_id_calls_database_execute(self):
        get_latest_challenge_from_player_id(1)
        self.db.execute.assert_called_once_with(
            "SELECT `id` FROM `challenges` WHERE (`p1`={0} OR `p2`={0}) AND `winner` is  NULL ORDER BY `id` LIMIT 1".format(
                self.player_model.id
            )
        )

    def test_get_latest_challenge_from_player_id_makes_correct_db_call_when_should_be_completed_passed(self):
        get_latest_challenge_from_player_id(1, should_be_completed=True)
        self.db.execute.assert_called_once_with(
            "SELECT `id` FROM `challenges` WHERE (`p1`={0} OR `p2`={0}) AND `winner` is NOT NULL ORDER BY `id` LIMIT 1".format(
                self.player_model.id
            )
        )

    def test_get_latest_challenge_from_player_id_calls_database_fetchone(self):
        get_latest_challenge_from_player_id(1)
        self.db.fetchone.assert_called_once_with()

    def test_get_latest_challenge_from_player_id_returns_challenge_model(self):
        ret = get_latest_challenge_from_player_id(1)
        self.challenge.assert_called_once_with(self.db.fetchone.return_value[0])
        self.assertEqual(ret, self.challenge.return_value)

    def test_get_latest_challenge_from_player_id_raises_player_exception_if_player_is_not_challenged(self):
        self.player_model.challenged = False
        with self.assertRaises(PlayerException) as e:
            get_latest_challenge_from_player_id(1)
        self.assertEqual(e.exception.args[0], "Player {} is currently not in an active challenge".format(self.player_model.gamertag))

    def test_get_latest_challenge_from_player_id_does_not_raise_exception_if_player_not_challenged_and_should_be_completed_passed(self):
        self.player_model.challenged = False
        get_latest_challenge_from_player_id(1, should_be_completed=True)

    def test_get_latest_challenge_from_player_id_raises_player_exception_if_rowcount_does_not_equal_one(self):
        self.db.rowcount = 2
        with self.assertRaises(PlayerException) as e:
            get_latest_challenge_from_player_id(1)
        self.assertEqual(e.exception.args[0], "Excepting 1 rows to be returned by DB, got 2 rows instead")
