import time
from os3_rrl.mysql.db import Database

db = Database()


class Player:
    def __init__(self, gamertag):
        playerinfo = Player.get_player_info(gamertag)
        self.id = playerinfo['pid']
        self.gamertag = gamertag
        self.rank = playerinfo['rank']
        self.challenged = playerinfo['challenged']
        self.timeout = playerinfo['challenged']

    def create_challenge(self, p2):
        opponent = Player(p2)
        self.challenged = opponent.id
        opponent.challenged = self.id

    def get_rank(self):
        return self.rank

    def set_rank(self, rank):
        # Write to database
        self.rank = rank

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, t):
        # Write to database
        self.timeout = t

    def clear_timeout(self):
        self.timeout = int(time.time())

    @staticmethod
    def get_player_info(gamertag):
        db.execute('SELECT id, gamertag, rank, challenged, UNIX_TIMESTAMP(timeout) FROM users WHERE gamertag="{}"'
                   .format(gamertag))
        res = db.fetchone()
        return {"pid": res[0], "gamertag": res[1], "rank": res[2], "challenged": res[3], "timeout": res[4]}

    @staticmethod
    def get_gamertag_by_id(id):
        db.execute('SELECT gamertag FROM users WHERE id={}'.format(id))
        res = db.fetchone()
        return res[0]

    @staticmethod
    def get_id_by_gamertag(gamertag):
        db.execute('SELECT gamertag FROM users WHERE gamertag="{}"'.format(gamertag))
        res = db.fetchone()
        return res[0]

    def __repr__(self):
        return self.gamertag.__str__
