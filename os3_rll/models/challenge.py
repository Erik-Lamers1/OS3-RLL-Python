from logging import getLogger
from datetime import datetime

from os3_rll.models.db import Database

logger = getLogger(__name__)


class ChallengeException(RuntimeError):
    pass


class Challenge:
    def __init__(self, i=0):
        self._id = i
        self.db = Database()
        self._date = 0
        self._p1 = 0
        self._p2 = 0
        self._p1_score = 0
        self._p2_score = 0
        self._winner = 0
        self._new = True if self._id == 0 else False
        if not self._new:
            self._date, self._p1, self._p2, self._p1_score, self._p2_score, self._winner = \
                self.get_challenge_info_from_db()
        if self._date:
            self._date = datetime.fromtimestamp(self._date)
        else
            self._date = datetime.now()

    def __enter__(self):
        return self

    @staticmethod
    def get_latest_challenge_from_player(p1, p2, should_be_completed=False):
        """
        Tries to find the latest challenge from a player
        param int p1: The player id that corresponds to the p1 column in the DB
        param int p2: The player id that corresponds to the p2 column in the DB
        param bool should_be_completed: If the challenge should already by completed
        returns int: id from the last challenge if found
        raises ChallengeException: if no challenge was found
        """
        with Database() as db:
            db.execute_prepared_statement(
                'SELECT id FROM challenges WHERE p1=%s AND p2=%s AND winner IS {} NULL ORDER BY id DESC'.format(
                    '' if should_be_completed else 'NOT'
                ),
                (p1, p2)
            )
            if db.rowcount != 1:
                raise ChallengeException('Challenge not found, or duplicate challenges found')
            return db.fetchone()[0]

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        """
        Set the challenge date from a datetime object
        param datetime.datetime() date: The datetime to set the date to
        """
        if not isinstance(date, datetime):
            raise ChallengeException('Date can only be set to a datetime.datetime() object')
        self._date = date

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1):
        if p1 < 0:
            raise ChallengeException("p1 can't be lower then 0")
        self._p1 = int(p1)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        if p2 < 0:
            raise ChallengeException("p2 can't be lower then 0")
        self._p2 = int(p2)

    @property
    def p1_score(self):
        return self._p1_score

    @p1_score.setter
    def p1_score(self, p1_score):
        if p1_score < 0:
            raise ChallengeException("p1_score can't be lower then 0")
        self._p1_score = p1_score

    @property
    def p2_score(self):
        return self._p2_score

    @p2_score.setter
    def p2_score(self, p2_score):
        if p2_score < 0:
            raise ChallengeException("p2_score can't be lower then 0")
        self._p2_score = p2_score

    @property
    def winner(self):
        if self._p1_score and self._p2_score:
            if self._p1_score > self._p2_score:
                self._winner = self._p1
            else:
                self._winner = self._p2
        return self._winner

    @winner.setter
    def winner(self, winner):
        raise ChallengeException('Winner cannot be set, please set p1_score and p2_score instead and the winner will be calculated')

    def get_challenge_info_from_db(self):
        logger.debug('Getting challenge info for challenge with id {} from DB'.format(self._id))
        self.db.execute_prepared_statement(
            'SELECT UNIX_TIMESTAMP(date), p1, p2, p1_score, p2_score, winner FROM challenges WHERE id=%s', (self._id,)
        )
        self._check_row_count()
        return self.db.fetchone()

    def _check_row_count(self, rowcount=1):
        if self.db.rowcount != rowcount:
            raise ChallengeException(
                'Excepting {} rows to be returned by DB, got {} rows instead'.format(rowcount, self.db.rowcount)
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
