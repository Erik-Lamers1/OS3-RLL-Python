import random
from logging import getLogger
from os3_rrl.conf import settings

logger = getLogger(__name__)


def test_call_int(*argv):
    logger.info('called: test_call_int()')
    return 42


def test_call_str(*argv):
    logger.info('called: test_call_str()')
    return "The answer to life the universe and everything is fourtytwo (42)\n"


def test_call_list(*argv):
    logger.info('called: test_call_list()')
    return ['SyntheticOxygen', 'Pandabeer', 'FrietWerk', 'Ronnierups', 'Mr.Vin']


def create_challenge(*argv):
    args = list(*argv)
    logger.info('called: stub.create_challenge')
    logger.info('called with: {}'.format(args))


def reset_challenge(*argv):
    args = list(*argv)
    logger.info('called: stub.reset_challenge')
    logger.info('called with: {}'.format(args))


def complete_challenge(*argv):
    args = list(*argv)
    logger.info('called: stub.complete_challenge')
    logger.info('called with: {}'.format(args))


def help(*argv):
    logger.info('called: stub.help')
    responses =['I cannot believe what a stupid FUCK you really are...\n Please do kill -9 $(pgrep yourself)\n',
                'Is it that difficult to type, do you have butter fingers?\n',
                'OH MY GOD you are stupid, please rm -rf ./your_life\n',
                "WHAHAHAHAHAhahahaHAHAHAA, seriously you can't even operate a normal discord bot.\n"]

    return random.choice(responses)
