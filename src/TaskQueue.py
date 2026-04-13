from typing import Iterable, Iterator, Callable
from src.Task import Task
class TaskQueue:
    def __init__(self,tasks: Iterable[Task]):
        """Инициализация"""
        self.tasks = list(tasks) if not isinstance(tasks, list) else tasks
    def __iter__(self) -> Iterator[Task]:
        """Реализация Итерации"""
        for task in self.tasks:
            yield task
    def __len__(self) -> int:
        """Длина очереди"""
        return sum(1 for task in self.tasks)
    def filter_by_priority(self, priority: str) -> 'TaskQueue':
        """Ленивый фильтр 1 создает новую очередь по приоритету """
        filtered = (t for t in self.tasks if t.priority == priority)
        return TaskQueue(filtered)
    def filter_by_status(self, status: str) -> 'TaskQueue':
        """Ленивый фильтр 2 по статусу"""
        filtered = (t for t in self.tasks if t.status == status)
        return TaskQueue(filtered)
