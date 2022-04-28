from configparser import ConfigParser

import psycopg2
from psycopg2 import pool


class ConnectionProvider:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        params = self.get_config()
        self.__connection_pool = psycopg2.pool.ThreadedConnectionPool(1, 10, **params)

    def get_connection(self):
        return self.__connection_pool.getconn()

    def free_connection(self, connection):
        self.__connection_pool.putconn(connection)

    def close(self):
        self.__connection_pool.closeall()

    def get_config(self):
        parser = ConfigParser()
        parser.read('database.ini')
        db = {}
        for param in parser.items('postgresql'):
            db[param[0]] = param[1]
        return db