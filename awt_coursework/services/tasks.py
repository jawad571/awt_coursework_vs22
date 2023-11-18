from repositories.tasks import Tasks as tasks_repository

class Tasks:
    def get_all_tasks(userId):
        return list(tasks_repository().get_all_tasks(userId=userId))

    def create_task(user_id, task_description):
        return tasks_repository().create_task(user_id, task_description)

    def get_task(task_id):
        return list(tasks_repository().get_task(task_id))[0]
        
    def update_task(task_id, task_description):
        return tasks_repository().update_task(task_id, task_description)

    def delete_task(task_id):
        return tasks_repository().delete_task(task_id)
    
    def get_db_status():
        return tasks_repository().get_db_status()