import asyncio
import unittest
import os
import json
import tempfile
from typing import List
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from src.TaskSource import TaskSource
from src.APITaskSource import APITaskSource
from src.AsyncTaskExecutor import AsyncTaskExecutor
from src.AsyncTaskQueue import AsyncTaskQueue
from src.GeneratorTaskSource import GeneratorTaskSource
from src.Task import Task
from src.FileTaskSource import FileTaskSource
from src.TaskQueue import TaskQueue
from src.descriptors import IdDescriptor, PriorityDescriptor, StatusDescriptor
from src.exceptions import TaskPriorityError, TaskIdError, TaskStateError, TaskDescriptionError,TaskStatusError
from src.handlers import EmailTaskHandler, ReportTaskHandler, DatabaseTaskHandler

class TestTask(unittest.TestCase):
    """Тесты TestTask"""
    def test_task_creation(self):
        """Тест создания задачи"""
        task = Task(id="test_task_1", description="first", priority="low")
        self.assertEqual(task.id, "test_task_1")
    def test_task_types(self):
        """Тест типов полей Task"""
        task = Task(id="123", description="value", priority="medium")
        self.assertIsInstance(task.id, str)

class TestFileTaskSource(unittest.TestCase):
    """Тесты  FileTaskSource"""
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
        self.test_task_data = [
            {"id": "file_test_1", "description": "first", "priority": "low"},
            {"id": "file_test_2", "description": "second", "priority": "high"}
        ]
        json.dump(self.test_task_data, self.test_file)
        self.test_file.close()
        self.source = FileTaskSource(self.test_file.name)

    def test_file_read(self):
        tasks = self.source.get_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, "first")
        self.assertEqual(tasks[1].priority, "high")

    def test_file_list(self):
        """ Тест что FileTaskSource возвращает список"""
        tasks = self.source.get_tasks()
        self.assertIsInstance(tasks, List)
    def test_file_object_task(self):
        """Тест что FileTaskSource возвращает объекты Task"""
        tasks = self.source.get_tasks()
        for task in tasks:
            self.assertIsInstance(task, Task)
    def test_fake_file(self):
        """Проверка отсутствующего файла"""
        source = FileTaskSource("fake_file.json")
        tasks = source.get_tasks()
        self.assertEqual(tasks, [])
    def test_empty_file(self):
        """Проверка бработка пустого файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8') as f:
            f.write("[]")
            f.flush()
            nema_file = FileTaskSource(f.name)
            tasks = nema_file.get_tasks()
            self.assertEqual(tasks, [])

class TestGeneratorTaskSource(unittest.TestCase):
    def test_generetion_list(self):
        """GeneratorTaskSource возвращает список"""
        source = GeneratorTaskSource(3)
        tasks = source.get_tasks()
        self.assertIsInstance(tasks, List)
    def test_generation_object_task(self):
        """GeneratorTaskSource возвращает объекты Task"""
        source = GeneratorTaskSource(3)
        tasks = source.get_tasks()
        for task in tasks:
            self.assertIsInstance(task, Task)

class TestAPITaskSource(unittest.TestCase):
    """Тесты для APITaskSource"""
    def setUp(self):
        """ Создаёт экземпляр APITaskSource """
        self.source = APITaskSource()
    def test_correct_count(self):
        """ APITaskSource возвращает необходимое количество задач"""
        tasks = self.source.get_tasks()
        self.assertEqual(len(tasks), 3)

    def test_api_list(self):
        """APITaskSource возвращает список"""
        tasks = self.source.get_tasks()
        self.assertIsInstance(tasks, List)

    def test_api_task(self):
        """APITaskSource возвращает объекты Task"""
        tasks = self.source.get_tasks()
        for task in tasks:
            self.assertIsInstance(task, Task)

class TestTaskSourceProtocol(unittest.TestCase):
    """Тесты протокола TaskSource"""
    def test_protocol(self):
        sources = [FileTaskSource("test.json"), GeneratorTaskSource(1), APITaskSource()]
        for s in sources:
            self.assertTrue(hasattr(s, 'get_tasks'))
    def test_subclasses(self):
        """Проверка что классы являются подклассами TaskSource"""
        classes = [FileTaskSource, GeneratorTaskSource, APITaskSource]
        for cls in classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(issubclass(cls, TaskSource))
    def test_non_sources(self):
        self.assertFalse(hasattr("строка", 'get_tasks'))


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


class TestAsync(IsolatedAsyncioTestCase):
    """Тестирование Асинхронного исполнителя задач"""
    async def asyncSetUp(self):
        self.queue = AsyncTaskQueue()
        self.executor = AsyncTaskExecutor(self.queue)

    async def test_queue(self):
        """Проверка работы очереди put и get"""
        task = Task(id="task_1", description="test", priority="low")
        await self.queue.put(task)
        result = await self.queue.get()
        self.assertEqual(result.id, "task_1")

    async def test_executor_registration_error(self):
        """Проверка регистрации строки вместо хэндлера"""
        with self.assertRaises(TypeError):
            self.executor.register_handler("email", "я просто строка")

    async def test_handler_crash(self):
        """Хэндлер выкидывает исключение"""
        mock_handler = AsyncMock()
        mock_handler.handle.side_effect = Exception("Сломалась")
        self.executor.register_handler("error_type", mock_handler)

        task = Task(id="fail_task", description="test", priority="high")
        task.task_type = "error_type"

        async with self.executor:
            await self.queue.put(task)
            await asyncio.sleep(0.1)

        self.assertEqual(task.status, "in_progress")

    async def test_executor_with_handlers(self):
        """Проверка работы экзекутора с хэндлерами"""
        handler = EmailTaskHandler()
        self.executor.register_handler("email", handler)

        task = Task(id="teest_taask", description="test", priority="medium")
        task.task_type = "email"

        async with self.executor:
            await self.queue.put(task)
            for _ in range(30):
                if task.status == "completed":
                    break
                await asyncio.sleep(0.05)
        self.assertEqual(task.status, "completed")

class TestHandlers(IsolatedAsyncioTestCase):
    """Тестирование реальных хэндлеров моих"""
    async def test_email_handler(self):
        handler = EmailTaskHandler()
        task = Task(id="email_task", description="test", priority="low")
        await handler.handle(task)
        self.assertTrue(True)

    async def test_report_handler(self):
        handler = ReportTaskHandler()
        task = Task(id="report_task", description="test", priority="high")
        await handler.handle(task)
        self.assertTrue(True)

    async def test_database_handler(self):
        handler = DatabaseTaskHandler()
        task = Task(id="databse_task", description="test", priority="critical")
        await handler.handle(task)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()