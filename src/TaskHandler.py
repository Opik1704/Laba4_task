from typing import runtime_checkable, Protocol

@runtime_checkable
class TaskHandler(Protocol):
    """
    Протокол определяющий контракт для асинхронных обработчиков задач
    """
    async def handle(self, task: dict) -> None:
        ...