import pymysql
from logging import getLogger

from os3_rrl.conf import settings

logger = getLogger(__name__)


class Database:
    def __init__(self):
        self.db_host = settings.DB_HOST
        self.db_user = settings.DB_USER
        self.db_pass = settings.DB_PASS
        self.db_database = settings.DB_DATABASE
        self.db = self.connect()
        self.cursor = self.db.cursor()

    def connect(self):
        logger.debug('Initializing connection to DB')
        return pymysql.connect(self.db_host, self.db_user, self.db_pass, self.db_database)

    def execute(self, query):
        self.cursor.execute(query)

    def execute_prepared_statement(self, query, parameters):
        """
        Execute a prepared statement on the DB
        :param str query: The SQL query in question (use %s for the placeholders)
        :param tuple parameters: The variables to place on the %s placeholders
        """
        self.cursor.execute(query, parameters)

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def commit(self):
        self.db.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.db.close()
