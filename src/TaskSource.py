from .Task import *
from  typing import *

@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол определяющий контракт для всех источников задач
    """
    def get_tasks(self) -> List[Task]:
        ...

