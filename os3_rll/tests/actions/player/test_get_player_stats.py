from unittest.mock import call

from os3_rll.tests import OS3RLLTestCase
from os3_rll.actions.player import get_player_stats
from os3_rll.tests.fixture import player_model_fixture


class TestGetPlayerStats(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_context_manager_patch("os3_rll.actions.player.Player")
        self.player.return_value = player_model_fixture()
        self.get_all_player_ids = self.set_up_patch("os3_rll.actions.player.get_all_player_ids_ordered")
        self.get_all_player_ids.return_value = [1]
        self.get_avg_goals = self.set_up_patch("os3_rll.actions.player.get_average_goals_per_challenge")
        self.get_avg_goals.return_value = 20

    def test_get_player_stats_calls_get_all_player_ids_ordered(self):
        get_player_stats()
        self.get_all_player_ids.assert_called_once_with()

    def test_get_player_stats_calls_player_model(self):
        get_player_stats()
        self.player.assert_called_once_with(self.get_all_player_ids.return_value[0])

    def test_get_player_stats_calls_get_average_goals_per_challenge(self):
        get_player_stats()
        self.get_avg_goals.assert_called_once_with(self.get_all_player_ids.return_value[0])

    def test_get_player_stats_returns_a_dict(self):
        self.assertIsInstance(get_player_stats(), dict)

    def test_get_player_stats_returns_player_stats_in_correct_format(self):
        s = get_player_stats()
        i = self.player.return_value.id
        self.assertEqual(s[i]["name"], self.player.return_value.gamertag)
        self.assertEqual(s[i]["discord"], self.player.return_value.discord)
        self.assertEqual(s[i]["rank"], self.player.return_value.rank)
        self.assertEqual(s[i]["wins"], self.player.return_value.wins)
        self.assertEqual(s[i]["losses"], self.player.return_value.losses)
        self.assertEqual(s[i]["is_challenged"], self.player.return_value.challenged)

    def test_get_player_stats_returns_average_goals_per_challenge(self):
        s = get_player_stats()
        self.assertEqual(s[self.player.return_value.id]["avg_goals_per_challenge"], self.get_avg_goals.return_value)
