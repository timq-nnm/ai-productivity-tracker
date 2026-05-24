from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime

from schemas.daily_entry import SDailyEntryAdd
from repositories.entry_repository import EntriesRepository
from .insights_service import InsightService

class EntriesService:
    @staticmethod
    async def create(entry: SDailyEntryAdd, session: AsyncSession):
        # Устанавливаем created_at если не указан
        data = entry.model_dump()
        if not data.get("created_at"):
            from datetime import datetime, timezone
            data["created_at"] = datetime.now(timezone.utc)

        saved_entry = await EntriesRepository.add_one(data, session)

        # Генерируем инсайт только если есть данные для анализа
        has_data = any([
            data.get("sleep"), data.get("energy"),
            data.get("clarity"), data.get("motivation"),
            data.get("reflection")
        ])
        if has_data:
            try:
                await InsightService.generate(saved_entry, session)  # type: ignore[arg-type]
            except Exception:
                pass  # LLM может не работать — не критично

        return saved_entry

    @staticmethod
    async def get_by_user(user_id: int, session: AsyncSession):
        user_entries = await EntriesRepository.get_by_user(user_id, session)
        return user_entries

    @staticmethod
    async def get_today_entry(user_id: int, session: AsyncSession):
        """Получить запись за сегодня."""
        today = date.today()
        return await EntriesRepository.get_by_date(user_id, today, session)

    @staticmethod
    async def update(entry_id: int, entry_data: SDailyEntryAdd, session: AsyncSession):
        """Обновить существующую запись."""
        await EntriesRepository.update_one(entry_id, entry_data.model_dump(), session)
        # Возвращаем обновлённую запись
        return await EntriesRepository.get_one(entry_id, session)