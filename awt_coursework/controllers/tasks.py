from services.tasks import Tasks as tasks_service

class Tasks:
    def get_all_tasks(userId):
        return tasks_service.get_all_tasks(userId=userId)

    def create_task(user_id, task_description):
        return tasks_service.create_task(user_id, task_description)

    def get_task(task_id):
        return tasks_service.get_task(task_id)
        
    def update_task(task_id, task_description):
        return tasks_service.update_task(task_id, task_description)

    def delete_task(task_id):
        return tasks_service.delete_task(task_id)
    
    def get_db_status():
        return tasks_service.get_db_status()