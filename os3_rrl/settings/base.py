import sys
from os import getenv

from unipath import Path

PROJECT_DIR = Path(__file__).absolute().ancestor(3)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            '()': 'os3_rrl.utils.logging.formatters.ConsoleFormatter',
            'fmt': '%(asctime)s [%(levelname)s] %(message)s',
            'colored': sys.stderr.isatty,  # StreamHandler uses stderr by default
        },
        'syslog': {
            'format': '[%(process)d] %(name)s [%(levelname)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
            'address': '/dev/log',  # remove this to use UDP port 514
        },
    },
    'loggers': {
        'saltyparrot': {
            'level': 'DEBUG',
        },
        'taskflow': {
            'level': 'WARNING',
        },
    },
    'root': {
        'handlers': ['console', 'syslog'],
        'level': 'DEBUG',
    }
}

DISCORD_TOKEN = getenv('DISCORD_TOKEN')
DISCORD_GUILD = getenv('DISCORD_GUILD', 'Cloud konijn')
DISCORD_CHANNEL = getenv('DISCORD_CHANNEL', 'rocket-league')
