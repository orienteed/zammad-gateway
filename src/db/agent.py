import sqlite3


class Agent():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Agent, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def __conect__(self):
        self.db_connection = sqlite3.connect(
            'db/users.db', check_same_thread=False)
        self.db_cursor = self.db_connection.cursor()

    def create(self, query):
        self.__conect__()
        self.db_cursor.execute(query)
        self.db_connection.commit()
        self.__disconect__()

    def read(self, query):
        self.__conect__()
        self.db_cursor.execute(query)
        user_data = self.db_cursor.fetchone()
        self.__disconect__()
        return user_data

    def update(self, query):
        self.__conect__()
        self.db_cursor.execute(query)
        self.db_connection.commit()
        self.__disconect__()

    def delete(self, query):
        self.__conect__()
        self.db_cursor.execute(query)
        self.db_connection.commit()
        self.__disconect__()

    def __disconect__(self):
        self.db_cursor.close()
