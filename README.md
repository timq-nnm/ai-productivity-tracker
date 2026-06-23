# 🧠 AI Productivity Tracking System

> AI-система для трекинга продуктивности, которая анализирует ежедневные данные пользователя (сон, энергия, мотивация, рефлексия) и превращает их в **инсайты, рекомендации и прогноз выгорания** с помощью LLM + RAG памяти.

---

## 🚀 One-liner

AI система, которая анализирует ежедневные данные о продуктивности пользователя и превращает их в инсайты и рекомендации с помощью **FastAPI + LangGraph + ChromaDB + GigaChat**.

---

## ❌ Проблема → ✅ Решение

### ❌ Проблема
Пользователь фиксирует своё состояние, но:
- не видит долгосрочные паттерны
- не понимает динамику энергии
- не замечает ранние признаки выгорания

### ✅ Решение
Система автоматически:
- собирает ежедневные данные
- анализирует их через LLM
- ищет похожие состояния через RAG (ChromaDB)
- формирует структурированные инсайты

---

## 🎬 Пример работы

```
Вход:
сон: 5
энергия: 4
мотивация: 3
рефлексия: "сильная усталость"

↓

RAG memory:
→ найдены похожие дни с низкой энергией

↓

LLM анализ:
→ выявлен негативный тренд

↓

Выход:
- Риск выгорания: HIGH
- Инсайт: снижение энергии последние 7 дней
- Рекомендации:
  • снизить нагрузку
  • добавить отдых
```

---

## 🧠 Возможности

- 📊 Ежедневный трекинг (сон, энергия, ясность, мотивация)
- 🤖 AI-анализ дня (GigaChat + LangGraph)
- 🧠 Долгосрочная память (ChromaDB RAG)
- 🔥 Детекция выгорания (rule-based + тренды)
- 📈 Анализ паттернов продуктивности
- 🔁 Streak tracking (серия дней)

---

## ⚙️ Архитектура

```
Client (Swagger / curl)
        ↓
FastAPI async backend
        ↓
   Service layer
        ↓
Repository layer (SQLAlchemy 2.0)
        ↓
       SQLite

LLM Pipeline (LangGraph)
├── memory_node (ChromaDB search)
├── analysis_node (GigaChat)
├── validate_node
└── parse_node
        ↓
  Structured Insight
        ↓
Database + Vector Store
```

---

## 🔄 LangGraph Pipeline

```
Entry created
   ↓
memory_node → поиск похожих дней
   ↓
analysis_node → генерация инсайтов
   ↓
validate_node → проверка ответа
   ↓
parse_node → Pydantic schema
   ↓
save → SQLite + ChromaDB
```

---

## 📦 Формат инсайта

```python
class DailyInsightSchema:
    summary: str
    recommendations: list[str]
    mood: str
    productivity_score: int  # 0–10
```

---

## 📊 Аналитика

### 🔥 Burnout detection
- NONE
- LOW
- MEDIUM
- HIGH
- CRITICAL

### 📈 Trend analysis
- сон
- энергия
- мотивация
- ясность

### 🔁 Streak
Подсчёт дней подряд с записями

---

## 🧱 Стек

| Слой    | Технология      |
| ------- | ---------------- |
| Backend | FastAPI (async)  |
| ORM     | SQLAlchemy 2.0   |
| LLM     | GigaChat         |
| Agent   | LangGraph        |
| Memory  | ChromaDB         |
| DB      | SQLite           |
| Testing | pytest           |

---

## 🚀 Быстрый старт

```bash
git clone https://github.com/timq-nnm/ai-productivity-tracker
cd ai-productivity-tracker

cp .env.example .env
# добавить GIGACHAT_API_KEY
```

```bash
docker-compose up -d --build
```

Открыть:

```
http://localhost:8888/docs
```

---

## 📡 API

### Users
- GET /api/v1/users
- POST /api/v1/users

### Entries
- POST /api/v1/entries
- GET /api/v1/entries/today/{user_id}

### Analytics
- GET /api/v1/analytics/burnout/{user_id}
- GET /api/v1/analytics/trends/{user_id}
- GET /api/v1/analytics/streak/{user_id}

### Insights
- GET /api/v1/insights/{user_id}

---

## 🧪 Тесты

```bash
pytest tests/ -v
```

Покрытие:
- CRUD пользователей
- CRUD записей
- аналитика (burnout, trends, streak)

---

## ⚖️ Tradeoffs

- LangGraph → контроль vs сложность
- RAG → качество vs latency
- async → масштабируемость vs дебаг

---

## 🔮 Будущее

- персонализация инсайтов
- прогноз продуктивности
- streaming анализа
- кеширование LLM
- мобильное приложение

---

## 🏷️ Tags

`fastapi` `langgraph` `llm` `rag` `chromadb` `gigachat` `async` `ai-productivity`