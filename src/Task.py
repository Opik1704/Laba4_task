from datetime import datetime

from src.descriptors import *
from src.exceptions import *

class Task:
    id = IdDescriptor()
    description = DescriptionDescriptor()
    priority = PriorityDescriptor()
    status = StatusDescriptor()

    icon = StatusIconDescriptor()

    task_type = TaskTypeDescriptor()

    def __init__(self, id:str, description:str,priority:str ,status:str = "pending"):
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.now()
        self._started_at: Optional[datetime] = None
        self._completed_at: Optional[datetime] = None
        task_type = "default"

    @property
    def created_at(self):
        """Время создания задачи"""
        return self._created_at
    @property
    def is_completed(self) -> bool:
        """Завершена ли задача."""
        return self.status == "completed"
    @property
    def is_ready(self) -> bool:
        """Возвращает задача готова или нет """
        return bool(self.description) and self.status != "completed"
    @property
    def age_seconds(self) -> float:
        """Возраст задачи в секундах"""
        return (datetime.now() - self._created_at).total_seconds()
    @property
    def age_minutes(self) -> float:
        """Возраст задачи в минутах"""
        return self.age_seconds / 60
    @property
    def age_hours(self) -> float:
        """Возраст задачи в часах"""
        return self.age_seconds / 3600
    @property
    def is_overdue(self) -> bool:
        """Просрочена ли задача """
        return self.age_hours > 1 and not self.is_completed

    def __repr__(self) -> str:
        return f"Task(id='{self.id}',{self.status},{self.priority})"

    def start(self):
        """Начать выполнение задачи"""
        if self.status == "in_progress":
            raise TaskStateError("Задача уже выполняется")
        if self.status == "pending":
            self.status = "in_progress"
            self._started_at = datetime.now()

    def complete(self):
        """Завершить выполнение задачи"""
        if self.status != "in_progress":
            raise TaskStateError("Завершить можно только выполняющуюся задачу")
        self.status = "completed"
        self._completed_at = datetime.now()

    def cancel(self):
        """Отменить задачу"""
        if self.status != "in_progress":
            raise TaskStateError("Отменить можно только выполняющуюся задачу")
        self.status = "pending"
        self._started_at = None
        self._completed_at = None
