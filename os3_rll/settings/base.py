import sys
from os import getenv

from unipath import Path

PYTHON_PACKAGE_NAME = 'os3-rocket-league-ladder'
PROJECT_DIR = Path(__file__).absolute().ancestor(3)
COGS_DIR = 'os3_rll/discord/cogs'

# Log settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            '()': 'os3_rll.utils.logging.formatters.ConsoleFormatter',
            'fmt': '%(asctime)s [%(name)8s] [%(levelname)s] %(message)s',
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
        'discord': {
            'level': 'INFO',
        },
        'websockets': {
            'level': 'INFO',
        }
    },
    'root': {
        'handlers': ['console', 'syslog'],
    }
}

# Discord settings
DISCORD_TOKEN = getenv('DISCORD_TOKEN')
DISCORD_GUILD = getenv('DISCORD_GUILD', 'Cloud konijn')
DISCORD_CHANNEL = getenv('DISCORD_CHANNEL', 'rocket-league')
WEBSITE = 'http://sheffield.studlab.os3.nl/OS3-Rocket-League-Ladder/'
DISCORD_EMBED_THUMBNAIL = 'https://rocketleague.media.zestyio.com/Rocket-League-Logo-Full_On-Dark-Vertical.f1cb27a519bdb5b6ed34049a5b86e317.png'

# Database settings
DB_HOST = '127.0.0.1'
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_DATABASE = getenv('DB_DATABASE', 'os3rl')
