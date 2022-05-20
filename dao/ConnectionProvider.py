from configparser import ConfigParser

import psycopg2
import threading
from psycopg2 import pool

instance = None

class ConnectionProvider:

    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super().__new__(cls)
    #     return cls.instance

    def __init__(self):
        params = self.get_config()
        self.__connection_pool = psycopg2.pool.ThreadedConnectionPool(1, 10, **params)
        self.__lock = threading.Lock()

    def get_connection(self):
        self.__lock.acquire()
        try:
            return self.__connection_pool.getconn()
        finally:
            self.__lock.release()

    def free_connection(self, connection):
        self.__lock.acquire()
        try:
            self.__connection_pool.putconn(connection)
        finally:
            self.__lock.release()

    def close(self):
        self.__connection_pool.closeall()

    def get_config(self):
        parser = ConfigParser()
        parser.read('database.ini')
        db = {}
        for param in parser.items('postgresql'):
            db[param[0]] = param[1]
        return db


def get_connection_provider():
    global instance
    if instance is None:
        instance = ConnectionProvider()
    return instance
