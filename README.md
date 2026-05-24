# 🧠 AI Productivity Tracking System

LLM-powered REST API для ежедневного трекинга продуктивности с AI-анализом через GigaChat и LangGraph.

> **Pet project** для резюме: FastAPI, async SQLAlchemy, LangGraph orchestration, GigaChat LLM, ChromaDB RAG, Docker, pytest.

---

## 🎯 О проекте

REST API собирает ежедневные данные о сне, энергии, ясности мышления и мотивации, анализирует паттерны через GigaChat и генерирует AI-инсайты с рекомендациями.

**Что умеет:**
- 📊 Ежедневный трекинг (сон, энергия, ясность, мотивация, задачи, рефлексия)
- 🤖 AI-анализ дня через GigaChat + LangGraph pipeline
- 🧠 Долгосрочная память через ChromaDB (RAG)
- 🔥 Детекция выгорания (rule-based + trend analysis)
- 📈 Аналитика паттернов продуктивности
- 📋 Streak tracking (серия дней)

---

## 🏗 Архитектура

```
HTTP Client (curl / Swagger UI)
         │
         ▼
FastAPI Backend (async)
         │
    ┌────┴────┐
    │         │
Services   LLM Layer
    │         │
Repos    LangGraph
    │     ┌───┴───┐
    │   Validate  Parse
    │     │       │
    │   Analysis Memory
    │         │
SQLite    ChromaDB
```

**Слои:**
| Слой | Папка | Описание |
|------|-------|---------|
| API | `api/v1/routes/` | FastAPI роутеры |
| Services | `services/` | Бизнес-логика |
| Repositories | `repositories/` | Data access layer (BaseRepository pattern) |
| Models | `models/` | SQLAlchemy 2.0 ORM (MappedAsDataclass) |
| Schemas | `schemas/` | Pydantic v2 validation |
| LLM | `llm/` | GigaChat + LangGraph workflow |
| Memory | `memory/` | ChromaDB vector store |

---

## 🛠 Стек

| Категория | Технологии |
|-----------|------------|
| **Backend** | FastAPI, SQLAlchemy 2.0 (async), Pydantic v2 |
| **LLM** | GigaChat (LangChain), LangGraph, Structured Output |
| **Database** | SQLite (file-based), ChromaDB (vectors) |
| **Testing** | pytest, pytest-asyncio, httpx |
| **Deploy** | Docker Compose |

---

## 🚀 Запуск

### Docker (рекомендуется)

```bash
# 1. Клонировать и настроить .env
git clone https://github.com/timq-nnm/ai-productivity-tracker
cd ai-productivity-tracker
cp .env.example .env
# Заполнить GIGACHAT_API_KEY в .env

# 2. Первый запуск
docker-compose up -d --build

# 3. Проверить
open http://localhost:8888/docs        # Swagger UI
docker-compose logs -f backend          # Логи
docker-compose ps                       # Статус

# 4. Остановить
docker-compose down
```

**Hot reload** — код монтируется через volume, изменения применяются мгновенно без пересборки. Пересборка нужна только при изменении `requirements.txt`.

---

## 📡 API Endpoints

### Пользователи
| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/users` | Все пользователи |
| `GET` | `/api/v1/users/{id}` | Пользователь по ID |
| `GET` | `/api/v1/users/by-username/{username}` | Поиск по username |
| `POST` | `/api/v1/users` | Создать пользователя |
| `DELETE` | `/api/v1/users/{id}` | Удалить пользователя |

### Записи (Daily Entries)
| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/entries/user/{user_id}` | Все записи пользователя |
| `GET` | `/api/v1/entries/today/{user_id}` | Запись за сегодня |
| `POST` | `/api/v1/entries` | Создать запись |
| `PUT` | `/api/v1/entries/{id}` | Обновить запись |

### Статистика
| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/stats/week/{user_id}` | Статистика за неделю |

### Аналитика
| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/analytics/burnout/{user_id}` | Риск выгорания |
| `GET` | `/api/v1/analytics/trends/{user_id}` | Тренды за период |
| `GET` | `/api/v1/analytics/patterns/{user_id}` | Паттерны продуктивности |
| `GET` | `/api/v1/analytics/streak/{user_id}` | Streak (серия дней) |

### Инсайты (AI)
| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/insights/{user_id}` | AI-инсайты пользователя |

---

## 📁 Структура проекта

```
ai-productivity-tracker/
├── main.py                    # FastAPI app entry point
├── config.py                  # Конфигурация (pydantic-settings)
├── requirements.txt
├── Dockerfile.backend
├── docker-compose.yml
├── pytest.ini
│
├── api/v1/routes/             # HTTP роутеры
│   ├── users.py
│   ├── entries.py
│   ├── stats.py
│   ├── analytics.py
│   └── insights.py
│
├── services/                  # Бизнес-логика
│   ├── users_service.py
│   ├── entry_service.py
│   ├── stats_service.py
│   ├── analytics_service.py
│   └── insights_service.py
│
├── repositories/              # Data access layer
│   ├── base_repository.py     # Generic CRUD
│   ├── user_repository.py
│   ├── entry_repository.py
│   └── insight_repository.py
│
├── models/                   # SQLAlchemy ORM
│   ├── user.py
│   ├── daily_entry.py
│   └── insight.py
│
├── schemas/                  # Pydantic v2 schemas
│   ├── user.py
│   ├── daily_entry.py
│   ├── insight.py
│   └── stat.py
│
├── llm/                      # LLM layer
│   ├── client.py             # GigaChat client
│   ├── prompts.py            # Prompt templates
│   ├── graph/                # LangGraph workflow
│   │   ├── state.py
│   │   └── workflow.py
│   ├── nodes/                # Graph nodes
│   │   ├── analysis_node.py
│   │   ├── memory_node.py
│   │   ├── parse_node.py
│   │   └── validate_node.py
│   └── schemas/              # LLM output schemas
│       └── insight.py
│
├── memory/                   # ChromaDB RAG
│   └── vector_store.py
│
├── core/                     # Инфраструктура
│   ├── database.py           # Async SQLAlchemy session
│   ├── lifespan.py           # App startup/shutdown
│   ├── exceptions/
│   └── handlers/
│
└── tests/                    # pytest tests
    ├── conftest.py
    ├── test_users.py
    ├── test_entries.py
    └── test_analytics.py
```

---

## 🔄 LLM Pipeline (LangGraph)

При создании записи с данными (сон/энергия/рефлексия) запускается LangGraph workflow:

```
Entry Created
     │
     ▼
[memory_node]     ← ChromaDB: поиск похожих записей
     │
     ▼
[analysis_node]   ← GigaChat: анализ дня + генерация инсайта
     │
     ▼
[validate_node]   ← Проверка структуры ответа
     │
     ▼
[parse_node]      ← Парсинг в Pydantic schema
     │
     ▼
Insight saved → ChromaDB indexed
```

**Structured Output:**
```python
class DailyInsightSchema(BaseModel):
    summary: str
    recommendations: list[str]
    mood: str
    productivity_score: int  # 0-10
```

---

## 📊 Аналитика

### Burnout Detection
Rule-based алгоритм на основе последних 7 дней:
- `NONE` → всё хорошо
- `LOW` → небольшое снижение
- `MEDIUM` → требует внимания
- `HIGH` / `CRITICAL` → срочно нужен отдых

### Trend Analysis
Сравнение первой и второй половины периода:
- Тренды по сну, энергии, ясности, мотивации
- `↑` / `↓` / `→` индикаторы

### Streak
Подсчёт непрерывной серии дней с записями.

---

## 🗄 База данных

SQLite (файл `data.db`). Таблицы создаются автоматически при первом запуске через `Model.metadata.create_all()`.

**users**
```sql
id          INTEGER PRIMARY KEY
username    VARCHAR UNIQUE NOT NULL
created_at  TIMESTAMP NOT NULL
```

**daily_entries**
```sql
id             INTEGER PRIMARY KEY
user_id        INTEGER REFERENCES users(id)
date           DATE NOT NULL
sleep          INTEGER        -- 0-10, nullable
energy         INTEGER        -- 0-10, nullable
clarity        INTEGER        -- 0-10, nullable
motivation     INTEGER        -- 0-10, nullable
tasks_planned  TEXT
tasks_done     TEXT
reflection     TEXT
created_at     TIMESTAMP
```

**insights**
```sql
id                 INTEGER PRIMARY KEY
user_id            INTEGER REFERENCES users(id)
entry_id           INTEGER REFERENCES daily_entries(id)
period_type        VARCHAR   -- daily / weekly
summary            TEXT
recommendations    TEXT
mood               VARCHAR
productivity_score INTEGER
created_at         TIMESTAMP
```

---

## 🧪 Тесты

14 smoke-тестов (pytest + httpx + in-memory SQLite):

```bash
# Запуск в Docker
docker exec ai-productivity-tracker-backend python -m pytest tests/ -v

# Или локально (нужны зависимости)
pip install pytest pytest-asyncio httpx aiosqlite
pytest tests/ -v
```

**Покрытие:** CRUD пользователей, CRUD записей, аналитика (burnout, streak, trends).

---

## ⚙️ Переменные окружения

| Переменная | Описание | Обязательно |
|-----------|----------|-------------|
| `GIGACHAT_API_KEY` | API ключ GigaChat | ✅ |
| `DATABASE_URL` | SQLite URL, по умолчанию `sqlite+aiosqlite:///./data.db` | — |
| `CHROMA_PATH` | Путь к ChromaDB, по умолчанию `./chroma_db` | — |
| `DEBUG` | Debug режим | — |

---

## 🧪 Пример запроса

```bash
# Создать пользователя
curl -X POST http://localhost:8888/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "nick"}'

# Создать запись
curl -X POST http://localhost:8888/api/v1/entries \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "date": "2026-05-24",
    "sleep": 7,
    "energy": 8,
    "clarity": 7,
    "motivation": 9,
    "tasks_planned": "написать тесты, code review",
    "reflection": "продуктивный день"
  }'

# Аналитика выгорания
curl http://localhost:8888/api/v1/analytics/burnout/1

# Streak
curl http://localhost:8888/api/v1/analytics/streak/1
```