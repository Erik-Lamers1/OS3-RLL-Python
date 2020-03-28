import logging
import logging.config

from os3_rrl.conf import settings


def setup_console_logging(verbosity=3):
    """
    :param int verbosity: Verbosity level, 0 being critical, 4 being debug
    """
    settings.LOGGING['handlers']['console']['level'] = logging.getLevelName(verbosity)
    logging.config.dictConfig(settings.LOGGING)
