from typing import List
import random

from src.Task import Task
from src.TaskSource import TaskSource


class GeneratorTaskSource:
    DESCRIPTIONS = ["Описание1","Описание2","Описание3","Описание4","Описание5"]
    PRIORITIES = ["low", "medium", "high", "critical"]
    STATUSES = ["pending", "in_progress", "completed", "failed"]
    def __init__(self, count:int) -> None:
        self.count = count
    def get_tasks(self) -> List[Task]:
        """
           Генерирует указанное количество задач
        """
        tasks = []
        for i in range(self.count):
            task_id = f"gen_{random.randint(1000, 9999)}"
            description = random.choice(self.DESCRIPTIONS)
            priority = random.choice(self.PRIORITIES)
            status = random.choice(self.STATUSES)
            try:
                task = Task(id=task_id,description=description,priority=priority,status=status)
                tasks.append(task)
            except Exception:
                continue
        return tasks
