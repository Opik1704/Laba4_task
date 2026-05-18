from typing import Iterable, Iterator, Callable, Generator
from src.Task import Task

class TaskQueueIterator:
    """Настоящий(True) итератор для очереди задач """
    def __init__(self, tasks):
        """Инициализируем итератор"""
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> Iterator[Task]:
        """возвращает итератор"""
        return self

    def __next__(self) -> Task:
        """шаг итерации или StopIteration"""
        if not hasattr(self._tasks, '__len__') or not hasattr(self._tasks, '__getitem__'):
            raise StopIteration

        if self._index >= len(self._tasks):
            raise StopIteration
        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue:
    """Очередь задач и ленивая фильтрация"""
    def __init__(self,_tasks: Iterable[Task]):
        """Инициализация"""
        if _tasks is not None:
            self.tasks = _tasks
        else:
            self.tasks = []

    def add_task(self, task: Task) -> None:
        """Добавление задачи в очередь """
        if hasattr(self.tasks, 'append'):
            self.tasks.append(task)
        else:
            raise TypeError("Нельзя добавить задачу в ленивый потоковый источник")

    def __iter__(self) -> TaskQueueIterator:
        """Итерация """
        return TaskQueueIterator(self.tasks)

    def __len__(self) -> int:
        """Длина очереди"""
        if hasattr(self.tasks, '__len__'):
            return len(self.tasks)
        raise TypeError("Queue with lazy source doesn't support len()")

    def filter_by_status(self, status: str) -> Generator[Task, None, None]:
        """Ленивый фильтр по статусу"""
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(self, priority: str) -> Generator[Task, None, None]:
        """Ленивый фильтр по приоритету"""
        for task in self:
            if task.priority == priority:
                yield task
