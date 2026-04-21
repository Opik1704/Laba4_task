# Лабораторная работа №4

## Асинхронный исполнитель задач

## Структура проекта
Laba4_task
 <pre>
 ├── src/ # 
 │ ├── init.py # Инициализация 
 │ ├── Task.py # Модель задачи в виде dataclass
 │ ├── TaskQueue.py # Очередь
 │ ├── TaskSource.py # Протокол источника задач
 │ ├── FileTaskSource.py # Источник задач из файла
 │ ├── GeneratorTaskSource.py # Генератор задач
 │ ├── APITaskSource.py # API-заглушка
 │ ├── descriptors.py #Дескрипторы
 │ ├── exceptions.py # Исключения
 │ ├── AsyncTaskQueue.py # Асинхронная  очередь
 │ ├── AsyncTaskExecutor.py  # Асинхронный исполнитель задач
 │ ├── TaskHandler.py # Протокол контракта обработчика
 │ ├── handlers.py # Реализации обработчиков (Email, Report, DB)
 │ └── main.py # точка входа в программу
 │
 ├── tests/ # Тесты
 │ ├── init.py # Инициализация тестов
 │ ├── test.py # Тесты 
 ├── .gitignore 
 ├── .pre-commit-config.yaml
 ├── pyproject.toml
 ├── README.md
 ├── requirements.txt
 ├── tasks.json 
 └── uv.lock
  </pre>
  
## Все сделано асинхронная очередь задач, описание контракта обработчика через Protocol, использование контекстных менеджеров для управления ресурсами, wентрализованное логирование и обработка ошибок;

## Тесты 92%
<img width="744" height="311" alt="image" src="https://github.com/user-attachments/assets/4310d369-eb19-4083-a0f0-6e2c3e9ac863" />


## Установка 
 ```bash
 $ python -m venv venv
 $ source venv/bin/activate
 
 $ pip install requirements.txt
 $ python -m src.main
```
