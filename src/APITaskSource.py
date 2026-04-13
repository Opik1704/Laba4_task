from src.TaskSource import TaskSource
from src.Task import Task

class APITaskSource:
    """
    API-заглушка, имитирующая внешний источник задач
    """
    def __init__(self, endpoint: str = "https://google.com/tasks")->None:
        """Создание фейковых тасков которые должны передатся с апи"""
        self.endpoint = endpoint
        self.mock_data = [
            { "id": "api_task_1","description": "Описание смешное","priority": "high","status": "pending"},
            { "id": "api_task_2","description": "Описание несмешное","priority": "medium","status": "in_progress"},
            { "id": "api_task_3","description": "Обновление документации","priority": "low", "status": "pending"}
        ]
    def get_tasks(self):
        """
          Имитирует получение задач от внешнего API.
          """
        try:
            tasks = []
            for task in self.mock_data:
                tasks.append(Task(
                    id=task["id"],
                    description=task["description"],
                    priority=task["priority"],
                    status=task["status"]
                ))
            return tasks
        except Exception as e:
            print("Ошибка",e)
            return []