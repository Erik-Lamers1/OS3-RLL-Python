import logging
import logging.config

from os3_rll.conf import settings


def setup_console_logging(verbosity=logging.INFO):
    """
    :param int verbosity: Verbosity level logging.<verbosity>
    """
    settings.LOGGING['handlers']['console']['level'] = verbosity
    logging.config.dictConfig(settings.LOGGING)
