from os3_rll.tests import OS3RLLTestCase
from os3_rll.operations.challenge import process_completed_challenge_args
from os3_rll.models.challenge import ChallengeException


class TestProcessCompletedChallengeArgs(OS3RLLTestCase):
    def test_process_completed_challenge_args_returns_a_tuple_of_four_values(self):
        results = process_completed_challenge_args("5-3")
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 4)

    def test_process_completed_challenge_args_returns_integers(self):
        [self.assertIsInstance(r, int) for r in process_completed_challenge_args("8-2")]

    def test_process_completed_challenge_args_raises_challenge_exception_if_invalid_match_result_passed(self):
        with self.assertRaises(ChallengeException) as e:
            process_completed_challenge_args("5-5-5")
        self.assertEqual(e.exception.args[0], "Unable to parse challenge arguments")

    def test_process_completed_challenge_args_parses_single_match_successfully(self):
        results = process_completed_challenge_args("5-4")
        self.assertEqual(results, (1, 0, 5, 4))

    def test_process_completed_challenge_args_parses_multiple_matches_successfully(self):
        results = process_completed_challenge_args("3-4 5-2 20-10")
        self.assertEqual(results, (2, 1, 28, 16))

    def test_process_completed_challenge_args_filters_out_none_values(self):
        results = process_completed_challenge_args("4-3      5-3 ")
        self.assertEqual(results, (2, 0, 9, 6))

    def test_process_completed_challenge_args_raises_challenge_exception_on_draw(self):
        with self.assertRaises(ChallengeException) as e:
            process_completed_challenge_args("3-4 4-3 2-1 3-5")
        self.assertEqual(e.exception.args[0], "Draws are not allowed")
