from unittest.mock import call

from os3_rll.tests import OS3RLLTestCase
from os3_rll.actions.player import get_player_ranking
from os3_rll.models.db import DBException


class TestGetPlayerRanking(OS3RLLTestCase):
    def setUp(self) -> None:
        self.db = self.set_up_context_manager_patch("os3_rll.actions.player.Database")
        self.db.return_value.__enter__.return_value.fetchall.return_value = (
            ("bert", 1, "bertje123"),
            ("jaap", 2, "jaapie"),
            ("henk", 3, "theMan"),
        )

    def test_get_player_ranking_makes_correct_db_calls(self):
        get_player_ranking()
        calls = [call(), call().execute("SELECT discord, rank, gamertag FROM users WHERE rank > 0 ORDER BY rank"), call().fetchall()]
        self.db.assert_has_calls(calls)

    def test_get_player_ranking_returns_dict(self):
        self.assertIsInstance(get_player_ranking(), dict)

    def test_get_player_ranking_returns_dict_of_player_rankings(self):
        r = get_player_ranking()
        for i, (key, value) in enumerate(r.items()):
            self.assertEqual(self.db.return_value.__enter__.return_value.fetchall.return_value[i][0], key)
            self.assertEqual(self.db.return_value.__enter__.return_value.fetchall.return_value[i][1:], value)

    def test_get_player_ranking_throws_db_exception_when_no_rows_are_returned(self):
        self.db.return_value.__enter__.return_value.rowcount = 0
        with self.assertRaises(DBException):
            get_player_ranking()
