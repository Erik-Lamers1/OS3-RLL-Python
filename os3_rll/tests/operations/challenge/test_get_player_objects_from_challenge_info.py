from unittest.mock import call

from os3_rll.operations.challenge import get_player_objects_from_challenge_info
from os3_rll.tests import OS3RLLTestCase
from os3_rll.models.challenge import ChallengeException


class TestGetPlayerObjectsFromChallengeInfo(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.operations.challenge.Player")
        self.player.get_player_id_by_username.return_value = 1
        self.db = self.set_up_context_manager_patch("os3_rll.operations.challenge.Database")
        self.db.return_value.__enter__.return_value.fetchone.return_value = (1, 2)

    def test_get_player_objects_from_challenge_info_makes_correct_player_model_calls(self):
        calls = [call.get_player_id_by_username("str", discord_name=True), call(1), call(2)]
        get_player_objects_from_challenge_info("str")
        self.player.assert_has_calls(calls)

    def test_get_player_objects_from_challenge_info_does_not_call_get_player_id_by_username_if_int_passed(self):
        get_player_objects_from_challenge_info(1)
        self.assertFalse(self.player.get_player_id_by_username.called)

    def test_get_player_objects_from_challenge_info_makes_correct_database_calls(self):
        calls = [
            call(),
            call().execute_prepared_statement(
                "SELECT p1, p2 FROM challenges WHERE (p1=%s OR p2=%s) AND winner IS  NULL ORDER BY id DESC", (1, 1)
            ),
            call().fetchone(),
        ]
        get_player_objects_from_challenge_info(1)
        self.db.assert_has_calls(calls)

    def test_get_player_objects_from_challenge_info_makes_correct_database_call_when_should_be_completed_passed(self):
        get_player_objects_from_challenge_info(1, should_be_completed=True)
        self.db().execute_prepared_statement.assert_called_once_with(
            "SELECT p1, p2 FROM challenges WHERE (p1=%s OR p2=%s) " "AND winner IS NOT NULL ORDER BY id DESC", (1, 1)
        )

    def test_get_player_objects_from_challenge_info_raises_challenge_exception_if_rowcount_is_0(self):
        self.db.return_value.__enter__.return_value.rowcount = 0
        with self.assertRaises(ChallengeException) as e:
            get_player_objects_from_challenge_info(1)
        self.assertEqual(e.exception.args[0], "No challenges found")
