from unittest import TestCase, mock
from pathlib import Path

from os3_rll.conf import settings


class OS3RLLTestCase(TestCase):
    destpath = None
    tempfile = None

    def __init__(self, *args, **kwargs):
        self.expected_git_path = Path(settings.PROJECT_DIR, ".git")
        self.assertTrue(self.expected_git_path.is_dir(), "project_path is not correct? (no .git found)")
        super(OS3RLLTestCase, self).__init__(*args, **kwargs)

    def set_up_patch(self, topatch, themock=None, **kwargs):
        """
        Patch a function or class
        :param topatch: string The class to patch
        :param themock: optional object to use as mock
        :return: mocked object
        """
        if themock is None:
            themock = mock.Mock()

        if "return_value" in kwargs:
            themock.return_value = kwargs["return_value"]

        patcher = mock.patch(topatch, themock)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def set_up_context_manager_patch(self, topatch, themock=None, **kwargs):
        patcher = self.set_up_patch(topatch, themock=themock, **kwargs)
        patcher.return_value.__exit__ = lambda a, b, c, d: None
        patcher.return_value.__enter__ = lambda x: None
        return patcher
