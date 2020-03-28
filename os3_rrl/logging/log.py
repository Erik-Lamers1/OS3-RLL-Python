import logging
import logging.config

from os3_rrl.conf import settings

def get_logging_verbosity(args=None, default_verbosity=3):
    """
    Return verbosity level from logging based a default verbosity, optionally
    adjusted with an offset determined by command-line arguments.
    :param argparse.Namespace args: Parsed command-line arguments
    :param int default_verbosity: Default verbosity
    :rtype: int
    """
    levels = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG
    }
    args_verbosity = 0 if args is None else sum(args.verbosity)
    return levels[min(max(args_verbosity + default_verbosity, 0), len(levels) - 1)]


def setup_console_logging(args=None, default_verbosity=3):
    """Configure logging to console using an ArgumentParser result
    Use a parser result from a parser that has verbosity arguments added with add_verbosity_args.
    By default it shows INFO and up, but by specifying the default verbosity this can be
    adjusted.
    :param argparse.Namespace args: Command line arguments
    :param int default_verbosity: Verbosity level, 0 being critical, 4 being debug
    """
    verbosity = get_logging_verbosity(args, default_verbosity=default_verbosity)
    settings.LOGGING['handlers']['console']['level'] = logging.getLevelName(verbosity)
    logging.config.dictConfig(settings.LOGGING)
