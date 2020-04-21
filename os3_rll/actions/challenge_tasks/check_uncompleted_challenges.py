from logging import getLogger

from os3_rll.models.db import Database
from os3_rll.discord.queue import discord_message_queue
from os3_rll.discord.announcements.challenge import announce_expired_challenge
from os3_rll.operations.utils import check_date_is_older_than_x_days
from os3_rll.actions.challenge import get_challenge, complete_challenge

logger = getLogger(__name__)


def check_uncompleted_challenges():
    """
    Checks for expired uncompleted challenges and completes them
    """
    with Database() as db:
        logger.info("Checking for expired challenges")
        db.execute("SELECT id, date, p1, p2 FROM challenges WHERE winner is NULL")
        challenges = db.fetchall()
        for challenge in challenges:
            logger.info("Challenge {} is passed the deadline, completing it".format(challenge[0]))
            if check_date_is_older_than_x_days(challenge[1], 7):
                # Challenge expired
                # Complete the challenge
                complete_challenge(int(challenge[2]), int(challenge[3]), "1-0", may_be_expired=True)
                # Announce the expired challenge to discord
                info = get_challenge(int(challenge[2]), should_be_completed=True)
                message = announce_expired_challenge(info)
                discord_message_queue.put(message)
                logger.info("Challenge {} has been completed".format(challenge[0]))
