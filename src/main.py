import asyncio
import logging

from src.AsyncTaskExecutor import AsyncTaskExecutor
from src.AsyncTaskQueue import AsyncTaskQueue
from src.APITaskSource import APITaskSource
from src.handlers import EmailTaskHandler, ReportTaskHandler, DatabaseTaskHandler


async def main():
    """Вход в приложение и создание tasks и вызов методов"""
    logging.basicConfig(level=logging.INFO)

    async_queue = AsyncTaskQueue()
    executor = AsyncTaskExecutor(async_queue)

    executor.register_handler("email", EmailTaskHandler())
    executor.register_handler("report", ReportTaskHandler())
    executor.register_handler("database", DatabaseTaskHandler())


    source = APITaskSource()
    tasks = source.get_tasks()

    tasks[0].task_type = "email"
    tasks[1].task_type = "report"
    tasks[2].task_type = "database"

    async with executor:
        for t in tasks:
            await async_queue.put(t)

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
