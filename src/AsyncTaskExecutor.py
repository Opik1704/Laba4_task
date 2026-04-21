import asyncio
import logging
from typing import Dict

from src.TaskHandler import TaskHandler
from src import AsyncTaskQueue

logger = logging.getLogger(__name__)

class AsyncTaskExecutor:
    """Асинхронный исполнитель задач с поддержкой разных обработчиков"""
    def __init__(self,queue: AsyncTaskQueue) -> None:
        self.queue = queue
        self.handlers:Dict[str,TaskHandler] = {}
        self._running = False

    def register_handler(self, task_type: str,handler: TaskHandler) -> None:
        """Регистрирует обработчик"""
        if not isinstance(handler,TaskHandler):
            raise TypeError("Обработчик должен реализовывать TaskHandler")
        self.handlers[task_type] = handler
        logger.info(f"Зарегистрирован обработчик для типа: {task_type}")

    async def _worker(self) -> None:
        """Рабочий обрабатывает задачи"""
        self._running = True
        logger.info("Worker запущен")
        while self._running:
            task = await self.queue.get()
            logger.info(f"Worker получил задачу {task.id}")

            task_type = getattr(task, 'task_type', 'default')
            handler = self.handlers.get(task_type)

            try:
                task.start()
                await handler.handle(task)
                task.complete()
                logger.info(f"Задача {task.id} успешно выполнена")
            except Exception as e:
                logger.error(f"Ошибка для задачи {task.id}: {e}")
            finally:
                self.queue.task_done()

    async def __aenter__(self):
        """ запускает воркер"""
        logger.info("Исполнитель запускается")
        self._main_task = asyncio.create_task(self._worker())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """останавливает воркер"""
        logger.info("Исполнитель завершает работу")
        if self._main_task:
            self._main_task.cancel()
            try:
                await self._main_task
            except asyncio.CancelledError:
                pass