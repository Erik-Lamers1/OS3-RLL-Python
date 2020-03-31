from datetime import datetime
from logging import getLogger
from hashlib import sha256

from os3_rll.models.db import Database

logger = getLogger(__name__)


class PlayerException(RuntimeError):
    pass


class Player:
    """
    A model of a player in the Database. This class holds all the relevant information in the Database and allows the
    operator to change them.

    This class will hold a local copy of the Player object.
    When self.save() is called the changes are written to the database
    If this class is called in a with block it will save the object automatically if force is set to True
    """

    def __init__(self, i=0, force=False):
        """
        param int id: The id of the player to assign this instance to. 0 means a new player.
        """
        self.db = Database()
        self._id = i
        self._name = ''
        self._rank = 0
        self._gamertag = ''
        self._discord = ''
        self._wins = 0
        self._losses = 0
        self._challenged = 0
        self._timeout = 0
        self._password = None
        self.force = force  # Force save when closing
        self._new = True if self._id == 0 else False
        if not self._new:
            self._name, self._rank, self._gamertag, self._discord, self._wins, self._losses, self._challenged, \
                self._timeout = self.get_player_info_from_db()
        self.original = (
            self._name, self._rank, self._gamertag, self._discord, self._wins, self._losses, self._challenged,
            self._timeout
        )
        if self._timeout:
            self.timeout = datetime.fromtimestamp(self._timeout)
        else:
            self.timeout = datetime.now()

    def __enter__(self):
        return self

    @staticmethod
    def get_player_id_by_gamertag(gamertag):
        """
        Use this function to get the player id from a gamertag
        param str gamertag: The gamertag to search for
        """
        with Database() as db:
            db.execute_prepared_statement('SELECT id FROM users WHERE gamertag=%s', (gamertag,))
            if db.rowcount != 1:
                raise PlayerException('Player not found, or to many players found')
            return db.fetchone()[0]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        if rank < 0:
            raise PlayerException("Rank can't be lower then 0")
        self._rank = int(rank)

    @property
    def gamertag(self):
        return self._gamertag

    @gamertag.setter
    def gamertag(self, gamertag):
        self._gamertag = str(gamertag)

    @property
    def discord(self):
        return self._discord

    @discord.setter
    def discord(self, discord):
        self._discord = discord

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, wins):
        if wins < 0:
            raise PlayerException("Wins can't be lower then 0")
        self._wins = int(wins)

    @property
    def losses(self):
        return self._losses

    @losses.setter
    def losses(self, losses):
        if losses < 0:
            raise PlayerException("Losses can't be lower then 0")
        self._losses = int(losses)

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """
        Set the player timeout from a datatime object
        param datatime.datetime() timeout: The datetime to set the player timeout to
        """
        if not isinstance(timeout, datetime):
            raise PlayerException('Timeout can only be set to a datetime.datetime object')
        self._timeout = timeout

    @property
    def challenged(self):
        return self._challenged == 1

    @challenged.setter
    def challenged(self, challenged):
        """
        param bool challenged: if the player is currently being challenged or not
        """
        self._challenged = 1 if challenged else 0

    @property
    def password(self):
        raise PlayerException("Passwords can't be retrieved")

    @password.setter
    def password(self, password):
        """
        Saves a hash of the passed password in the player model
        """
        logger.debug('Generating SHA256 hash from player password')
        self._password = sha256(password.encode('utf-8')).hexdigest()

    def save(self):
        if self._new:
            self._save_new_player()
        else:
            if self.check_if_player_info_has_changed():
                if not self.force:
                    raise PlayerException(
                        'Database info has changed between the creation of this instance and now, '
                        'retry of force instead'
                    )
                else:
                    logger.warning('Database info has changed between the creation of this instance and now, '
                                   'forcing save')
            self._save_existing_player_model()
        logger.debug('Committing player model change to stable storage')
        self.db.commit()

    def _save_existing_player_model(self):
        self.db.execute_prepared_statement(
            'UPDATE users SET name=%s, gamertag=%s, discord=%s, rank=%s, wins=%s, losses=%s, '
            'challenged=%s, timeout=%s WHERE id=%s',
            (self._name, self._gamertag, self._discord, self._rank, self._wins, self._losses, self._challenged,
             self._timeout.strftime("%Y-%m-%d %H:%M:%S"), self._id)
        )

    def _save_new_player(self):
        # Check if any of the required vars is None
        if any(arg is None for arg in (self._name, self._gamertag, self._password)):
            raise PlayerException(
                'Unable to save player object without required properties, please provide name, gamertag and password'
            )
        if not self._discord:
            self._discord = self._gamertag
        logger.info('Inserting new player into DB')
        self.db.execute_prepared_statement(
            'INSERT INTO users SET name=%s, gamertag=%s, discord=%s, password=%s',
            (self._name, self._gamertag, self._discord, self._password)
        )

    def _check_row_count(self, rowcount=1):
        if self.db.rowcount != rowcount:
            raise PlayerException(
                'Excepting {} rows to be returned by DB, got {} rows instead'.format(rowcount, self.db.rowcount)
            )

    def check_if_player_info_has_changed(self):
        logger.debug('Checking if player info has changed')
        player_info = self.get_player_info_from_db()
        return True if player_info != self.original else False

    def get_player_info_from_db(self):
        logger.debug('Getting player info for player with id {} from db'.format(self._id))
        self.db.execute_prepared_statement(
            'SELECT name, rank, gamertag, discord, wins, losses, challenged, UNIX_TIMESTAMP(timeout) '
            'FROM users WHERE id=%s',
            (self._id,)
        )
        self._check_row_count()
        return self.db.fetchone()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.force:
            self.save()
        self.db.close()
