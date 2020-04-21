from os3_rll.tests import OS3RLLTestCase
from os3_rll.rocket_league_ladder import parse_args


class TestRLLParseArgs(OS3RLLTestCase):
    def test_parse_args_returns_false_values_by_default(self):
        args = parse_args()
        self.assertFalse(args.verbose)
        self.assertFalse(args.version)

    def test_parse_args_sets_verbose_to_true_when_passed(self):
        args = parse_args(["--verbose"])
        self.assertTrue(args.verbose)

    def test_parse_args_sets_version_to_true_when_passed(self):
        args = parse_args(["--version"])
        self.assertTrue(args.version)

    def test_parse_args_can_handle_both_args_when_passed(self):
        args = parse_args(["--version", "--verbose"])
        self.assertTrue(args.verbose)
        self.assertTrue(args.version)
