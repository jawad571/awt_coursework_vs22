from database.mongo_db_connection import MongoDBConnection
from database.schemas import Schemas
from database.validate import Validate

class Users:
    _instance = None
    _db_flag = False
    temp_db = []
    id_counter = 0

    def __new__(self):
        if not self._instance:
            try:
                self._instance = super().__new__(self)
                self.db_reference = MongoDBConnection().get_database()
                self.collection = self.db_reference['users']
                self._db_flag = True
            except:
                print("Failed to get DB")
        return self._instance

    def get_all_users(self):
        if self._db_flag:
            result = self.collection.find({})
            return result
        else:
            return self.temp_db
    
    def get_user(self, username):
        if self._db_flag:
            result = self.collection.find({"username": username})
            return result
        else:
            return [i for i in self.temp_db if i['username'] == username]
    
    def create_user(self, username, password):
        if self._db_flag:
            payload = {
                "username": username,
                "password": password
            }
            self.collection.insert_one(payload)
        else:
            self.temp_db.append({
                "_id": self.id_counter,
                "username": username,
                "password": password
            })
            self.id_counter = self.id_counter + 1
        
    def get_db_status(self,):
        return self._db_flag