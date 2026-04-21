import asyncio
import logging
from collections import deque
from typing import Deque, List

from src import Task

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AsyncTaskQueue:
    """Асинхронная очередь задач"""
    def __init__(self):
        self._queue:Deque[Task] = deque()
        self._condition = asyncio.Condition()

    async def put(self, task: Task) -> None:
        """ДОбавить задачу в очередь"""
        async with self._condition:
            self._queue.append(task)
            self._condition.notify()

    async def get(self) -> Task:
        """Получить задачу из очереди"""
        async with self._condition:
            while not self._queue:
                await self._condition.wait()
            return self._queue.popleft()

    def task_done(self):
        pass