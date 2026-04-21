import json
import logging
from typing import List

from src.Task import Task
from src.TaskSource import TaskSource

logger = logging.getLogger(__name__)
class FileTaskSource:
    """
    Читает задачи из Json файла
    """
    def __init__(self, filename:str)->None:
        self.filename = filename

    def get_tasks(self) -> List[Task]:
        """
        Читает задачи из JSON файла и преобразует их в объекты Task
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            tasks = []
            for item in data:
                try:
                    task = Task(id=item["id"],description=item.get("description", ""),priority=item.get("priority", "medium"),status=item.get("status", "pending")
                    )
                    tasks.append(task)
                except Exception as e:
                    logger.warning(f"Пропущена некорректная задача в файле: {e}")
                    continue
            return tasks
        except FileNotFoundError:
            logger.error(f"Файл {self.filename} не найден")
            return []
        except json.JSONDecodeError:
            logger.error(f"Файл {self.filename} имеет некорректный формат JSON")
            return []
        except Exception as e:
            logger.error("Ошибка",e)
            return []
