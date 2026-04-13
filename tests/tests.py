import unittest
import os
import json
import tempfile
from src.Task import Task
from src.FileTaskSource import FileTaskSource
from src.TaskQueue import TaskQueue
from src.descriptors import IdDescriptor, PriorityDescriptor, StatusDescriptor
from src.exceptions import TaskPriorityError, TaskIdError, TaskStateError, TaskDescriptionError,TaskStatusError


class TestDescriptors(unittest.TestCase):
    """Тестирование дескрипторов и методов"""

    def test_valid_priority(self):
        """Проверка правильных приоритетов"""
        for p in ["low", "medium", "high", "critical"]:
            with self.subTest(priority=p):
                task = Task(id="test", description="desc", priority= p )
                self.assertEqual(task.priority, p)

    def test_invalid_priority_raises(self):
        """Проверка неправильного приоритета"""
        with self.assertRaises(TaskPriorityError):
            Task(id="test", description="desc", priority="fake")

        with self.assertRaises(TaskPriorityError):
            Task(id="test", description="desc", priority=123)

    def test_status_icon_logic(self):
        """Проверка иконок (Non-Data дескриптора)"""
        task = Task(id="T1", description="Test", priority="medium")
        self.assertEqual(task.icon, "⏳")

        task.start()
        self.assertEqual(task.icon, "🚀")

        task.complete()
        self.assertEqual(task.icon, "✅")

    def test_state_transitions(self):
        """Проверка статуса"""
        task = Task(id="T1", description="Test", priority="low")
        with self.assertRaises(TaskStateError):
            task.complete()

    def test_task_time_properties(self):
        """Проверка времени"""
        task = Task(id="T_TIME", description="Time test", priority="low")
        self.assertGreaterEqual(task.age_minutes, 0)
        self.assertGreaterEqual(task.age_hours, 0)

    def test_task_overdue_logic(self):
        """Проверка is_overdue"""
        task = Task(id="T_OVERDUE", description="Overdue test", priority="medium")
        self.assertFalse(task.is_overdue)

    def test_task_cancel_logic(self):
        """Проверка отмены задачи"""
        task = Task(id="T_CANCEL", description="Cancel test", priority="high")
        task.start()
        task.cancel()
        self.assertEqual(task.status, "pending")

    def test_descriptor_class_access(self):
        """Проверка доступа через класс """
        self.assertIsInstance(Task.id, IdDescriptor)
        self.assertIsInstance(Task.priority, PriorityDescriptor)

    def test_invalid_description_type(self):
        """Проверка  описания"""
        task = Task(id="T_DESC", description="Desc", priority="low")
        with self.assertRaises(TaskDescriptionError):
            task.description = 1000

class TestTaskSources(unittest.TestCase):
    """Проверка получение задачи """
    def test_list_source_success(self):
        """Проверка создания задач из обычного списка словарей."""
        data = [
            {"id": "1", "description": "first", "priority": "low"},
            {"id": "2", "description": "Second", "priority": "high"}
        ]
        tasks = [Task(**item) for item in data]

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1].priority, "high")
        self.assertEqual(tasks[0].id, "1")

    def test_bad_source(self):
        """Неправмильную задачу передали """
        data = [
            {"id": "1", "description": "Good", "priority": "low"},
            {"id": "2", "description": "Bad", "priority": "fake"}
        ]
        tasks = []
        for item in data:
            try:
                tasks.append(Task(**item))
            except (TaskPriorityError, TaskIdError, TaskDescriptionError):
                continue

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, "1")

    def test_file_source_empty_if_no_file(self):
        """Отсутвие файла"""
        source = FileTaskSource("not_exists.json")
        self.assertEqual(source.get_tasks(), [])

class TestTaskQueue(unittest.TestCase):
    """Тестирование ленивой очереди задач"""

    def setUp(self):
        """Подготовка задач"""
        self.raw_tasks = [
            Task(id="T1", description="High Task", priority="high"),
            Task(id="T2", description="Low Task", priority="low"),
            Task(id="T3", description="Another High", priority="high"),
        ]
        self.queue = TaskQueue(self.raw_tasks)

    def test_iteration_protocol(self):
        """Проверка реализации итерации"""
        tasks_list = list(self.queue)
        self.assertEqual(len(tasks_list), 3)
        self.assertIsInstance(tasks_list[0], Task)

    def test_lazy_filters(self):
        """Проверка фильтрации по приоритету и статусу"""
        high_prio_queue = self.queue.filter_by_priority("high")

        self.assertIsInstance(high_prio_queue, TaskQueue)
        results = list(high_prio_queue)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(t.priority == "high" for t in results))

    def test_multiple_iterations(self):
        """Проверка поддержки повторного обхода очереди"""
        first_pass = [t.id for t in self.queue]
        second_pass = [t.id for t in self.queue]

        self.assertEqual(first_pass, second_pass, "Очередь 'опустела' после первого прохода!")
        self.assertEqual(len(second_pass), 3)

    def test_chained_filters(self):
        """Проверка цепочки ленивых фильтров"""
        self.raw_tasks[0].start()

        pipeline = self.queue.filter_by_priority("high").filter_by_status("in_progress")

        results = list(pipeline)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "T1")

    def test_empty_results(self):
        """Проверка фильтрации, если такого нет"""
        empty_queue = self.queue.filter_by_priority("critical")
        self.assertEqual(len(list(empty_queue)), 0)

    def test_big_data_simulation(self):
        """Проверка ленивости"""
        big_tasks_gen = (Task(id=f"T{i}", description="D", priority="low") for i in range(1000))
        queue = TaskQueue(big_tasks_gen)

        filtered = queue.filter_by_priority("high")
        self.assertEqual(len(list(filtered)), 0)

if __name__ == "__main__":
    unittest.main()