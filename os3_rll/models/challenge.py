from logging import getLogger
from datetime import datetime

from os3_rll.models.db import Database

logger = getLogger(__name__)


class ChallengeException(RuntimeError):
    pass


class Challenge:
    """
    The Challenge model allows a operator to get or create a challenge from the DB and interface with it
    This class will hold a local copy of the Player object
    When self.save() is called the changes are written to the database
    """
    def __init__(self, i=0, force=False):
        """
        param int i: The id of the challenge to get, if left to 0 a new challenge will be created
        param bool force: Set the force parameter to True to enable certain (dangerous) operations,
            Like auto-saving on __exit__, overwriting changed DB values and resetting or deleting a challenge
        """
        # Set force to true to force a model save on __exit__ and disregard DB changes
        self.force = force
        self._id = i
        self.db = Database()
        self._date = 0
        self._p1 = None
        self._p2 = None
        self._p1_wins = None
        self._p2_wins = None
        self._p1_score = 0
        self._p2_score = 0
        self._winner = 0
        self._new = True if self._id == 0 else False
        if not self._new:
            self._date, self._p1, self._p2, self._p1_wins, self._p2_wins, self._p1_score, self._p2_score, \
                self._winner = self.get_challenge_info_from_db()
        self.original = (
            self._date,
            self._p1,
            self._p2,
            self._p1_wins,
            self._p2_wins,
            self._p1_score,
            self._p2_score,
            self._winner
        )
        if self._date:
            self._date = datetime.fromtimestamp(self._date)
        else:
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
                'SELECT id FROM challenges WHERE p1=%s AND p2=%s AND winner IS {} NULL ORDER BY id DESC LIMIT 1'.format(
                    'NOT' if should_be_completed else ''
                ),
                (p1, p2)
            )
            # Check for non existing challenge
            if db.rowcount != 1:
                raise ChallengeException('Challenge not found')
            return db.fetchone()[0]

    @property
    def id(self):
        return self._id

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
        if p1 == self.p2:
            raise ChallengeException("Id of p1 can't be equal to p2")
        self._p1 = int(p1)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        if p2 < 0:
            raise ChallengeException("p2 can't be lower then 0")
        if p2 == self.p1:
            raise ChallengeException("Id of p2 can't be equal to p1")
        self._p2 = int(p2)

    @property
    def p1_wins(self):
        return self._p1_wins

    @p1_wins.setter
    def p1_wins(self, wins):
        if wins < 0:
            raise ChallengeException("p1_wins can't be lower then 0")
        if wins == self.p2_wins:
            raise ChallengeException("p1_wins can't be equal to p2_wins")
        self._p1_wins = wins

    @property
    def p2_wins(self):
        return self._p2_wins

    @p2_wins.setter
    def p2_wins(self, wins):
        if wins < 0:
            raise ChallengeException("p2_wins can't be lower then 0")
        if wins == self.p1_wins:
            raise ChallengeException("p2_wins can't be equal to p1_wins")
        self._p2_wins = wins

    @property
    def p1_score(self):
        return self._p1_score

    @p1_score.setter
    def p1_score(self, p1_score):
        if p1_score < 0:
            raise ChallengeException("p1_score can't be lower then 0")
        if p1_score == self.p2_score:
            raise ChallengeException("p1_score can't be equal to the score of player 2")
        self._p1_score = p1_score

    @property
    def p2_score(self):
        return self._p2_score

    @p2_score.setter
    def p2_score(self, p2_score):
        if p2_score < 0:
            raise ChallengeException("p2_score can't be lower then 0")
        if p2_score == self.p1_score:
            raise ChallengeException("p2_score can't be equal to the score of player 1")
        self._p2_score = p2_score

    @property
    def winner(self):
        # Explicitly check for int, because 0 is also a valid number
        if isinstance(self._p1_wins, int) and isinstance(self._p2_wins, int):
            if self._p1_wins > self._p2_wins:
                self._winner = self._p1
            else:
                self._winner = self._p2
        return int(self._winner)

    @winner.setter
    def winner(self, winner):
        raise ChallengeException(
            'Winner cannot be set, please set p1_wins and p2_wins instead and the winner will be calculated'
        )

    def save(self):
        if self._new:
            self._save_new_challenge()
        else:
            if self.check_if_challenge_info_has_changed():
                if not self.force:
                    raise ChallengeException(
                        'DB info has changed while trying to save, refusing save. Set force=True to overwrite'
                    )
                else:
                    logger.warning('DB info has changed! Force enabled, overwriting DB info...')
            self._save_existing_challenge_model()
        self.db.commit()

    def _save_new_challenge(self):
        # Check if any of the required args are missing
        if any(arg is None for arg in (self._p1, self._p2)):
            raise ChallengeException('When creating a new challenge the p1, and p2 properties are required')
        logger.info('Inserting new challenge into DB')
        self.db.execute_prepared_statement(
            'INSERT INTO challenges SET date=%s, p1=%s, p2=%s', (self._date, self._p1, self._p2)
        )

    def _save_existing_challenge_model(self):
        logger.info('Updating DB for challenge with id {}'.format(self._id))
        # Check the actual winner property so if the user didn't set it we still appoint a winner
        self.db.execute_prepared_statement(
            'UPDATE challenges SET date=%s, p1=%s, p2=%s, p1_wins=%s, p2_wins=%s, p1_score=%s, p2_score=%s, winner=%s '
            'WHERE id=%s',
            (
                self._date,
                self._p1,
                self._p2,
                self._p1_wins,
                self._p2_wins,
                self._p1_score,
                self._p2_score,
                self.winner,
                self._id
            )
        )

    def reset(self):
        """
        Reset a challenge
        This will clear the scores of p1 and p2 and the winner value
        """
        # First check if force is set
        if not self.force:
            raise ChallengeException('Resetting a challenge requires the parameter flag to be set')
        if self._new:
            raise ChallengeException('New challenges cannot be reset')
        logger.info('Resetting the scores of challenge {}'.format(self._id))
        self.db.execute_prepared_statement(
            'UPDATE challenges SET p1_wins=NULL, p2_wins=NULL, p1_score=NULL, p2_score=NULL, winner=NULL WHERE id=%s',
            (self._id,)
        )
        logger.info('Reloading myself')
        self.db.commit()
        self.__init__(i=self._id, force=self.force)

    def delete(self):
        """
        Delete the challenge associated with this instance
        """
        if not self.force:
            raise ChallengeException('Deleting a challenge requires the force parameter to be set')
        if self._new:
            raise ChallengeException('New challenges cannot be deleted')
        logger.info('Deleting challenge with id {}'.format(self._id))
        self.db.execute_prepared_statement('DELETE FROM challenges WHERE id=%s', (self._id,))
        self.db.commit()

    def get_challenge_info_from_db(self):
        logger.debug('Getting challenge info for challenge with id {} from DB'.format(self._id))
        self.db.execute_prepared_statement(
            'SELECT UNIX_TIMESTAMP(date), p1, p2, p1_wins, p2_wins, p1_score, p2_score, winner FROM challenges '
            'WHERE id=%s',
            (self._id,)
        )
        self._check_row_count()
        return self.db.fetchone()

    def check_if_challenge_info_has_changed(self):
        logger.debug('Checking if challenge info has changed')
        challenge_info = self.get_challenge_info_from_db()
        return True if challenge_info != self.original else False

    def _check_row_count(self, rowcount=1):
        if self.db.rowcount != rowcount:
            raise ChallengeException(
                'Excepting {} rows to be returned by DB, got {} rows instead'.format(rowcount, self.db.rowcount)
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.force:
            self.save()
        self.db.close()
