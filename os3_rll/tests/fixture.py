from datetime import datetime
from unittest.mock import Mock

from os3_rll.models.player import Player
from os3_rll.models.challenge import Challenge


def player_model_fixture(db_mock=Mock(), **kwargs):
    """
    Get a player model fixture which can be manipulated at will
    All values passed will be set to the player fixture

    param unittest.mock db_mock: The mock object to use for the database object inside the player model
    """
    p = Player(offline=True)
    p._id = 1
    p._new = False
    p.db = db_mock
    p.name = "Henk"
    p.gamertag = "testGamertag"
    p.discord = "testDiscord"
    p.rank = 1
    p.wins = 1
    p.losses = 1
    p.timeout = datetime.now()
    p.challenged = False
    p.password = "test"
    for key, value in kwargs.items():
        if not hasattr(p, key):
            raise KeyError("Unknown player model attribute: {}".format(key))
        setattr(p, key, value)
    return p


def challenge_model_fixture(db_mock=Mock(), **kwargs):
    """
    Get a challenge model fixture which can be manipulated at will
    All values passed will be set to the challenge fixture

    param unittest.mock db_mock: The mock object to use for the database object inside the challenge model
    """
    c = Challenge(offline=True)
    c._id = 1
    c._new = False
    c.db = db_mock
    c.p1 = 1
    c.p2 = 2
    c.p1_score = 10
    c.p2_score = 20
    c.p1_wins = 1
    c.p2_wins = 2
    c.date = datetime.now()
    for key, value in kwargs.items():
        if not hasattr(c, key):
            raise KeyError("Unknown challenge model attribute: {}".format(key))
        setattr(c, key, value)
    return c
