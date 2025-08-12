# EduPlatform Test Framework
[![CI][ci-badge]][ci-url] [![Python][py-badge]][py-url] [![Coverage][cov-badge]][cov-url]

[ci-badge]: https://github.com/Pankirbor/autotests-api/actions/workflows/tests.yml/badge.svg
[ci-url]: https://github.com/Pankirbor/autotests-api/actions
[py-badge]: https://img.shields.io/badge/Python-3.11%2B-blue?logo=python

## 📌 Технологии

- **Python** - *язык программирования*
- **pytest** - *тестовый фреймворк*
- **Faker** - *для имитации реальных данных*
- **Allure** - *для отчётов*
- **Swagger Coverage Tool** - *для анализа покрытия API*
- **HTTPX** - *для HTTP-запросов*
- **Pydantic** - *для валидации данных*

---

## 🔍 Обзор проекта
Этот проект представляет собой автоматизированную систему тестирования API для учебного сервера курсов. Основная цель - комплексная проверка REST API приложения для обеспечения его стабильности и соответствия требованиям.

### 🔧 Ключевые особенности реализации

В проекте применяются современные практики автоматизированного тестирования:

- **Специализированные API-клиенты** для структурированного взаимодействия с эндпоинтами
- **Pytest-фикстуры** для создания переиспользуемых тестовых окружений
- **Строгая валидация данных** через Pydantic модели
- **Проверка схем ответов** для контроля соблюдения API-контракта
- **Генерация тестовых данных** с помощью Faker для имитации реальных сценариев
- **Продвинутые техники тестирования** для повышения надежности и эффективности проверок

### 🏗 Архитектурные принципы

Проект организован в соответствии с лучшими отраслевыми стандартами, что обеспечивает:
- Четкую структуру кода
- Легкость поддержки и расширения
- Возможность масштабирования тестовой базы
- Прозрачность тестовых сценариев

### 🧪 Что проверяем

Автотесты покрывают все ключевые функциональные блоки API:
| Маршрут         | Описание               |
|-----------------|------------------------|
| `/users`        | Управление пользователями |
| `/files`        | Работа с файлами       |
| `/courses`      | Управление курсами     |
| `/exercises`    | Управление упражнениями |
| `/authentication` | Аутентификация        |

---

## ⚙️ Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/Pankirbor/autotests-api.git
cd autotests-api
```
### 2. Создание виртуального окружения.
#### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3 Установка зависимостей.
```bash
pip install -r requirements.txt
```
## 🚀 Запуск тестов
### ⚠️ Предварительные требования

Для полноценного запуска тестов необходимо предварительно развернуть тестируемый сервер:

```bash
git clone https://github.com/Nikita-Filonov/qa-automation-engineer-api-course.git
cd qa-automation-engineer-api-course
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001
```
### 1. Запуск всех тестов с генерацией Allure-отчёта
```bash
pytest --alluredir=./allure-results
allure serve allure-results
```

### 2. Запуск только регрессионных тестов
```bash
pytest -m "regression" --alluredir=./allure-results
```

### 3. Параллельный запуск тестов
```bash
pytest -n auto  # Использует pytest-xdist
```

## 📊 Отчёты и артефакты

### Allure-отчёт (публичная версия)
Актуальный отчёт доступен на GitHub Pages:
📌 [Открыть Allure-отчёт](https://pankirbor.github.io/autotests-api/)

### Покрытие API (артефакты CI/CD)
После каждого запуска тестов в CI/CD генерируется **Swagger Coverage Report** (артефакт)
   Доступен на странице Actions → последний workflow → "Artifacts"

## 🔗 Интеграция с CI/CD
Фреймворк поддерживает GitHub Actions для автоматического запуска тестов.
Конфигурация CI находится в .github/workflows/.

## 📬 Контакты
- Автор: [Pankirbor](https://github.com/Pankirbor)
- Тестируемый API: [Course Test Server](https://github.com/Nikita-Filonov/qa-automation-engineer-api-course)