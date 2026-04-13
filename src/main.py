from src.Task import Task
from src.TaskQueue import TaskQueue
from src.TaskSource import TaskSource
from src.FileTaskSource import FileTaskSource
from src.GeneratorTaskSource import GeneratorTaskSource
from src.APITaskSource import APITaskSource

from src.exceptions import TaskPriorityError, TaskIdError


def main():
    """Вход в приложение и создание tasks и вызов методов"""
    tasks = [
        Task(id="Task1", description="Первая задача", priority="high"),
        Task(id="Task2", description="Вторая задача", priority="low"),
        Task(id="Task3", description="Третья задача", priority="medium"),
        Task(id="Task1", description="Первая задача", priority="high"),
        Task(id="Task2", description="Вторая задача", priority="low"),
        Task(id="Task3", description="Третья задача", priority="medium"),
        Task(id="Task1", description="Первая задача", priority="high"),
        Task(id="Task2", description="Вторая задача", priority="low"),
        Task(id="Task3", description="Третья задача", priority="medium"),
    ]

    queue = TaskQueue(tasks)

    print("Первый обход (фильтрация)")
    high_prio = queue.filter_by_priority("high")
    for task in high_prio:
        print(f"Найдена {task.id} [{task.priority}]")

    print("\nПовторный обход (вся очередь через list)")
    all_tasks = list(queue)
    print(f"Количество задач при повторном обращении {len(all_tasks)}")

    for t in all_tasks:
        print(f"- {t.id}: {t.description}")

    low_count = sum(1 for _ in queue.filter_by_priority("low"))
    print(f"Количество задач с низким приоритетом: {low_count}")

if __name__ == "__main__":
    main()
