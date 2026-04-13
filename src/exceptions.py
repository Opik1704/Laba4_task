class TaskIdError(Exception):
    """Ошибка при неправильном идентификаторе задачи"""
    pass

class TaskDescriptionError(Exception):
    """Ошибка при неправильном описании задачи"""
    pass

class TaskPriorityError(Exception):
    """Ошибка при неправильном приоритете задачи"""
    pass

class TaskStatusError(Exception):
    """Ошибка при неправильном статусе задачи"""
    pass

class TaskStateError(Exception):
    """Ошибка при неправильном переходе состояния задачи"""
    pass
