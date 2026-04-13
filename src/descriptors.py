from typing import Optional, Any

from src.exceptions import *


class IdDescriptor:
    """Дескриптор для id"""
    def __init__(self):
        self._data = {}
    def __get__(self, obj, objtype=None)->Any:
        if obj is None:
            return self
        return obj.__dict__.get('_id', '')
    def __set__(self, obj, value)->None:
        if not isinstance(value, str):
            raise TaskIdError(f"ID должен быть строкой {type(value).__name__}")
        obj.__dict__['_id'] = value


class DescriptionDescriptor:
    """Дескриптор для  description."""
    def __init__(self):
        self._data = {}
    def __get__(self, obj, objtype=None)->Any:
        if obj is None:
            return self
        return obj.__dict__.get('_description', '')
    def __set__(self, obj, value: str)->None:
        if not isinstance(value, str):
            raise TaskDescriptionError(
                f"Описание должно быть строкой {type(value).__name__}"
            )
        if len(value) > 500:
            raise TaskDescriptionError(
                f"Описание должно быть менее 500 символов, получено {len(value)}"
            )
        obj.__dict__['_description'] = value
class PriorityDescriptor:
    """Дескриптор для priority"""
    VALID_PRIORITIES = {"low", "medium", "high", "critical"}

    def __get__(self, obj: Optional[object], objtype: Optional[type] = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get('_priority', 'medium')
    def __set__(self,obj,value:str)->None:
        if not isinstance(value,str):
            raise TaskPriorityError( f"Приоритет должен быть строкой, получен {type(value).__name__}")
        if value not in PriorityDescriptor.VALID_PRIORITIES:
            raise TaskPriorityError(f"Приоритет должен быть одним из {self.VALID_PRIORITIES}")
        obj.__dict__['_priority'] = value

class StatusDescriptor:
    """Дескриптор для status"""
    VALID_STATUSES = {"pending", "in_progress", "completed", "failed"}
    def __get__(self, obj: Optional[object], objtype: Optional[type] = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get('_status', 'pending')
    def __set__(self,obj,value)-> None:
        if not isinstance(value, str):
            raise TaskStatusError(f"Статус должен быть строкой {type(value).__name__}")
        if value not in StatusDescriptor.VALID_STATUSES:
            raise TaskStatusError(f"Статус должен быть одним из {self.VALID_STATUSES}")
        obj.__dict__['_status'] = value
class StatusIconDescriptor:
    """Non-data descriptor чтобы надо"""
    ICONS = {
        "pending": "⏳",
        "in_progress": "🚀",
        "completed": "✅",
        "failed": "❌"
    }
    def __get__(self, obj, objtype=None)-> Any:
        if obj is None:
            return self
        return self.ICONS.get(obj.status, "❓")

class TaskTypeDescriptor:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get('_task_type', 'default')
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("Тип задачи должен быть строкой")
        obj.__dict__['_task_type'] = value

