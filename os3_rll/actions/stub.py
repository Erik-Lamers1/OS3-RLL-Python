import random
from logging import getLogger
from collections import deque
from os3_rll.conf import settings

logger = getLogger(__name__)


def hello(*argv):
    args = deque(*argv)
    logger.debug('actions.stub.hello: called with: {}'.format(args))
    user = args.popleft()
    res = 'Hi {}\n'.format(user.mention)
    responses = ["How are you doing today? Wait that's retorical, I am a bot I do not care.\n",
                 "I was just looking at your rank. Did you know that you suck at rocket league? I heard some guy "
                 "SquishyMuffinz is best.\n",
                 "Please leave me alone. I am randomizing the rankings database to mess with Mr.Vin.\n",
                 "Due to COVID-19 I've had to reimplement the transport protocol from QUIC to plain UDP to avoid "
                 "handshakes.\n",
                 "Please do not bother me. I am looking into this Markov Chain theory. It should be able to give me "
                 "more human like responses.",
                 "What are you doing here? LOL, your rank is so low you should practice uninstall.\n"]
    res += random.choice(responses)
    return res

def test_call_int(*argv):
    logger.debug('actions.stub.test_call_int: called with {}'.format(*argv))
    return 42


def get_website(*argv):
    args = list(*argv)
    logger.debug('actions.stub.get_website: called with {}'.format(*argv))
    user = args[0].mention
    website = "http://sheffield.studlab.os3.nl/OS3-Rocket-League-Ladder/"
    return "{} you can find the website at {}".format(user, settings.WEBSITE)


def test_call_str(*argv):
    args = list(*argv)
    logger.debug('called: test_call_str()')
    return "Don't know, but the answer to life the universe and everything is fourtytwo (42)\n"


def test_call_list(*argv):
    logger.debug('called: test_call_list()')
    return ['Toekel', 'SyntheticOxygen', 'Pandabeer', 'FrietWerk', 'Ronnierups', 'Mr.Vin']


def create_challenge(*argv):
    args = list(*argv)
    logger.debug('called: stub.create_challenge')
    logger.debug('called with: {}'.format(args))


def reset_challenge(*argv):
    args = list(*argv)
    logger.debug('called: stub.reset_challenge')
    logger.debug('called with: {}'.format(args))


def complete_challenge(*argv):
    args = list(*argv)
    logger.debug('called: stub.complete_challenge')
    logger.debug('called with: {}'.format(args))


def stub_help(*argv):
    logger.debug('called: stub.help')
    responses =['I cannot believe what a stupid FUCK you really are...\n Please do kill -9 $(pgrep yourself)\n',
                'Is it that difficult to type, do you have butter fingers?\n',
                'OH MY GOD you are stupid, please rm -rf ./your_life\n',
                "WHAHAHAHAHAhahahaHAHAHAA, seriously you can't even operate a normal discord bot.\n"]

    return random.choice(responses)
