import pymongo
from constants.db import DB

connection_string = DB.connection_string.value
db_name = DB.database_name.value
class MongoDBConnection:
    _instance = None

    def __new__(self):
        if not self._instance:
            print(f'Initiating Mongodb connection using string: {connection_string}')
            self._instance = super().__new__(self)
            self._instance.client = pymongo.MongoClient(connection_string)
            print(f'Initializing Database {db_name}')
            self._instance.database = self._instance.client[db_name]
            print("Connnection established succesfully")
        return self._instance

    def get_database(self):
        return self.database