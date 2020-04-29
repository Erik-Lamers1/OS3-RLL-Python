from datetime import timedelta

from os3_rll.tests import OS3RLLTestCase
from os3_rll.tests.fixture import player_model_fixture, challenge_model_fixture
from os3_rll.actions.challenge import get_challenge
from os3_rll.models.challenge import ChallengeException


class TestGetChallenge(OS3RLLTestCase):
    def setUp(self) -> None:
        self.player = self.set_up_patch("os3_rll.actions.challenge.Player")
        self.player.return_value.get_player_id_by_username.return_value = 10
        self.challenge = self.set_up_patch("os3_rll.actions.challenge.get_latest_challenge_from_player_id")
        self.challenge.return_value = challenge_model_fixture()
        self.player_objs = self.set_up_patch("os3_rll.actions.challenge.get_player_objects_from_challenge_info")
        self.player_objs.return_value = (
            player_model_fixture(),
            player_model_fixture(name="Bert", _id=2, gamertag="bertje", discord="bert123", rank=2),
        )

    def test_get_challenges_calls_player_model_when_string_is_passed(self):
        get_challenge("blaap")
        self.player.get_player_id_by_username.assert_called_once_with("blaap", discord_name=True)

    def test_get_challenge_calls_player_model_without_searching_for_discord_name(self):
        get_challenge("blaap", search_by_discord_name=False)
        self.player.get_player_id_by_username.assert_called_once_with("blaap", discord_name=False)

    def test_get_challenge_does_not_call_player_model_if_no_str_was_passed(self):
        get_challenge(1)
        self.assertFalse(self.player.get_player_id_by_username.called)

    def test_get_challenge_calls_get_latest_challenge_from_player_id(self):
        get_challenge(1)
        self.challenge.assert_called_once_with(1, should_be_completed=False)

    def test_get_challenge_calls_get_latest_challenge_from_player_id_with_should_be_completed(self):
        get_challenge(1, should_be_completed=True)
        self.challenge.assert_called_once_with(1, should_be_completed=True)

    def test_get_challenge_calls_get_player_objects_from_challenge_info(self):
        get_challenge(1)
        self.player_objs.assert_called_once_with(1, should_be_completed=False)

    def test_get_challenge_calls_get_player_objects_from_challenge_info_with_should_be_completed(self):
        get_challenge(1, should_be_completed=True)
        self.player_objs.assert_called_once_with(1, should_be_completed=True)

    def test_get_challenge_catches_any_exception_on_player_model(self):
        self.player.get_player_id_by_username.side_effect = RuntimeError
        with self.assertRaises(ChallengeException):
            get_challenge("blaap")

    def test_get_challenge_catches_any_exception_on_get_latest_challenge(self):
        self.challenge.side_effect = KeyError
        with self.assertRaises(ChallengeException):
            get_challenge(1)

    def test_get_challenge_catches_any_exception_on_get_player_objects_from_challenge_info(self):
        self.player_objs.side_effect = IOError
        with self.assertRaises(ChallengeException):
            get_challenge(1)

    def test_get_challenge_gives_back_deadline_one_week_from_challenge_date(self):
        c = get_challenge(1)
        self.assertEqual(c["deadline"], self.challenge.return_value.date + timedelta(weeks=1))

    def test_get_challenge_returns_p1_from_challenge_info(self):
        c = get_challenge(1)
        self.assertEqual(c["p1"]["id"], self.player_objs.return_value[0].id)
        self.assertEqual(c["p1"]["rank"], self.player_objs.return_value[0].rank)
        self.assertEqual(c["p1"]["name"], self.player_objs.return_value[0].gamertag)
        self.assertEqual(c["p1"]["discord"], self.player_objs.return_value[0].discord)

    def test_get_challenge_returns_p2_from_challenge_info(self):
        c = get_challenge(1)
        self.assertEqual(c["p2"]["id"], self.player_objs.return_value[1].id)
        self.assertEqual(c["p2"]["rank"], self.player_objs.return_value[1].rank)
        self.assertEqual(c["p2"]["name"], self.player_objs.return_value[1].gamertag)
        self.assertEqual(c["p2"]["discord"], self.player_objs.return_value[1].discord)
