import random
from logging import getLogger
from os3_rll.conf import settings

logger = getLogger(__name__)


def test_call_int():
    logger.debug('called: test_call_int()')
    return "42"


def test_call_str():
    logger.debug('called: test_call_str()')
    return "The answer to life the universe and everything is fourtytwo (42)\n"


def test_call_list():
    logger.debug('called: test_call_list()')
    return ['SyntheticOxygen', 'Pandabeer', 'FrietWerk', 'Ronnierups', 'Mr.Vin']


def create_challenge(*argv):
    args = list(*argv)
    logger.debug('called: stub.create_challenge')
    logger.debug(f'called with: {args}')


def reset_challenge(*argv):
    args = list(*argv)
    logger.debug('called: stub.reset_challenge')
    logger.debug(f'called with: {args}')


def complete_challenge(*argv):
    args = list(*argv)
    logger.debug('called: stub.complete_challenge')
    logger.debug(f'called with: {args}')


def help():
    logger.debug('called: stub.help')
    responses =['I cannot believe what a stupid FUCK you really are...\n Please do kill -9 $(pgrep yourself)\n',
                'Is it that difficult to type, do you have butter fingers?\n',
                'OH MY GOD you are stupid, please rm -rf ./your_life\n',
                "WHAHAHAHAHAhahahaHAHAHAA, seriously you can't even operate a normal discord bot.\n"]

    return random.choice(responses)
