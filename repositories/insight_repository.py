from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from models.insight import InsightModel
from models.daily_entry import DailyEntryModel

class InsightRepository(BaseRepository):
    model = InsightModel

    @classmethod
    async def get_by_user(cls, user_id: int, session: AsyncSession):
        """Получить все инсайты пользователя с датой записи через JOIN."""
        query = (
            select(InsightModel, DailyEntryModel.date)
            .outerjoin(DailyEntryModel, InsightModel.entry_id == DailyEntryModel.id)
            .where(InsightModel.user_id == user_id)
            .order_by(InsightModel.created_at.desc())
        )

        result = await session.execute(query)
        rows = result.all()

        # Добавляем дату к каждому инсайту как атрибут
        insights = []
        for insight, entry_date in rows:
            insight._entry_date = entry_date  # type: ignore[attr-defined]
            insights.append(insight)

        return insights