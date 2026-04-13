import asyncio
import logging

from src.Task import Task

logger = logging.getLogger(__name__)

class EmailTaskHandler:
    """Обработчик для отправки email"""
    async def handle(self, task: dict) -> None:
        logger.info(f"Отправляюю email для задачи {task.id}")
        await asyncio.sleep(1)
        print(f"email для задачи {task.description} отправлен")

class ReportTaskHandler:
    """Обработчик для отчетов"""
    async def handle(self, task: Task) -> None:
        logger.info(f"Генерирую отчета для задачи {task.id}")
        await asyncio.sleep(1)
        print(f" Отчет для задачи {task.id} сделан ")

class DatabaseTaskHandler:
    """Обработчик сохранения данных в БД"""
    async def handle(self, task: Task) -> None:
        logger.info(f"Сохранение задачи {task.id} в базу данных")
        await asyncio.sleep(1)
        print(f" Задача {task.id} сохранена в БД +- ")