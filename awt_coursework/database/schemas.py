from enum import Enum

class Schemas(Enum):
    create_task_schema = {
        "type": "object",
        "properties": {
            "userId": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string", "enum": ['backlog', 'toDo', 'inProgress', 'done']}
        },
        "required": ["userId", "title", "description", "status"]
    }
    update_task_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string", "enum": ['backlog', 'toDo', 'inProgress', 'done']}
        },
    }    