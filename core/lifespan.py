from fastapi import FastAPI
from contextlib import asynccontextmanager
import os

from core.database import engine, Model
from models.daily_entry import DailyEntryModel
from models.insight import InsightModel
from models.user import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы (SQLite)
    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data.db")
    if "sqlite" in database_url:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
        print("SQLite: таблицы созданы")

    print("База данных готова к работе")

    yield

    print("Выключение сервера")
