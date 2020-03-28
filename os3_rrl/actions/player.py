import time


class Player:
    def __init__(self, gamertag):
        playerinfo = self.get_player_info(gamertag)
        self.id = playerinfo['pid']
        self.gamertag = playerinfo['gamertag']
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

    def get_player_info(self, gamertag):
        # 'SELECT id, gamertag, rank, challenged, UNIX_TIMESTAMP(timeout) FROM users WHERE gamertag={}'
        return {"pid": 1, "gamertag": '', "rank": '', "challenged": '', "timeout": ''}

    def __repr__(self):
        return self.gamertag.__str__
