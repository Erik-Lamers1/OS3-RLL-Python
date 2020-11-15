from unittest.mock import call

from os3_rll.tests import OS3RLLTestCase
from os3_rll.operations.player import get_all_player_ids_ordered
from os3_rll.models.db import DBException


class TestGetAllPlayerIdsOrdered(OS3RLLTestCase):
    def setUp(self) -> None:
        self.db = self.set_up_context_manager_patch("os3_rll.operations.player.Database")
        self.db.return_value.__enter__.return_value.rowcount = 1
        self.db.return_value.__enter__.return_value.fetchall.return_value = ((1,), (2,), (3,))

    def test_get_all_player_ids_ordered_makes_correct_database_model_calls(self):
        get_all_player_ids_ordered()
        calls = [
            call(),
            call().execute_prepared_statement("SELECT `id` FROM `users` ORDER BY %s", ("rank",)),
            call().fetchall(),
        ]
        self.db.assert_has_calls(calls)

    def test_get_all_players_ids_ordered_makes_correct_database_models_calls_when_order_by_passed(self):
        get_all_player_ids_ordered(order_by="banaan")
        calls = [
            call(),
            call().execute_prepared_statement("SELECT `id` FROM `users` ORDER BY %s", ("banaan",)),
            call().fetchall(),
        ]
        self.db.assert_has_calls(calls)

    def test_get_all_player_ids_ordered_raises_db_exception_when_rowcount_is_zero(self):
        self.db.return_value.__enter__.return_value.rowcount = 0
        with self.assertRaises(DBException) as e:
            get_all_player_ids_ordered()
        self.assertEqual(e.exception.args[0], "No users returned")

    def test_get_all_player_ids_ordered_returns_a_list(self):
        ret = get_all_player_ids_ordered()
        self.assertIsInstance(ret, list)

    def test_get_all_player_ids_ordered_returns_a_list_of_ids_returned_by_database(self):
        ret = get_all_player_ids_ordered()
        self.assertEqual(ret, [1, 2, 3])
