from database.mongo_db_connection import MongoDBConnection
from database.schemas import Schemas
from database.validate import Validate

class Tasks:
    _instance = None
    _db_flag = False
    temp_db = []
    id_counter = 0

    def __new__(self):
        if not self._instance:
            try:
                self._instance = super().__new__(self)
                self.db_reference = MongoDBConnection().get_database()
                self.collection = self.db_reference['tasks']
                self._db_flag = True
            except:
                print("Failed to get DB")
        return self._instance

    def get_all_tasks(self, userId):
        if self._db_flag:
            query = {"userId": userId}
            print(query)
            result = self.collection.find(query)
            return result
        else:
            return self.temp_db
    
    def get_task(self, task_id):
        if self._db_flag:
            result = self.collection.find({"_id": task_id})
            return result
        else:
            return [i for i in self.temp_db if i['_id'] == task_id]
    
    def create_task(self, user_id, task_description):
        if self._db_flag:
            payload = {
                "userId": user_id,
                **task_description
            }
            if Validate.validate_document(payload, Schemas.create_task_schema.value):
                self.collection.insert_one(payload)
            else:
                raise ValueError("Incorrect Schema for task description")
        else:
            self.temp_db.append({
                "userId": user_id,
                "_id": self.id_counter,
                **task_description
            })
            self.id_counter = self.id_counter + 1
        
    def update_task(self, task_id, task_description):
        if self._db_flag:
            if len(list(self.collection.find({"_id": task_id}))) < 1:
                raise ValueError("Task not found")
            
            if Validate.validate_document(task_description, Schemas.update_task_schema.value):
                self.collection.update_one({'_id': task_id}, {'$set':task_description})
            else:
                raise ValueError("Incorrect Schema for updating task description")
        else:
            for i in self.temp_db:
                if i['_id'] == task_id:
                    i = {
                        "_id": task_id,
                        **task_description
                    }

    def delete_task(self, task_id):
        if self._db_flag:
            self.collection.delete_one({'_id': task_id})
        else:
            self.temp_db = [i for i in self.temp_db if i['_id'] != task_id]

    def get_db_status(self,):
        return self._db_flag