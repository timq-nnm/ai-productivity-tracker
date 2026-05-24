from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from datetime import datetime, timedelta, date, timezone

from models.daily_entry import DailyEntryModel
from repositories.base_repository import BaseRepository

class EntriesRepository(BaseRepository):
    model = DailyEntryModel

    @classmethod
    async def get_by_period(cls, user_id: int, session: AsyncSession, days: int = 7):
        from_date = (datetime.now(timezone.utc) - timedelta(days=days)).date()

        query = select(DailyEntryModel).where(
            DailyEntryModel.user_id == user_id,
            DailyEntryModel.date >= from_date
        )

        result = await session.execute(query)

        return result.scalars().all()
    
    @classmethod
    async def get_by_user(cls, user_id: int, session: AsyncSession):
        query = select(DailyEntryModel).where(DailyEntryModel.user_id == user_id)

        result = await session.execute(query)

        return result.scalars().all()
    
    @classmethod
    async def get_by_date(cls, user_id: int, target_date: date, session: AsyncSession):
        """Получить запись пользователя за конкретную дату."""
        query = select(DailyEntryModel).where(
            DailyEntryModel.user_id == user_id,
            DailyEntryModel.date == target_date
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
