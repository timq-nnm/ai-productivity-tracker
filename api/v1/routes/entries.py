from fastapi import APIRouter, status, HTTPException
from datetime import date
from typing import Optional

from schemas.daily_entry import SDailyEntry, SDailyEntryAdd
from core.database import SessionDep
from services.entry_service import EntriesService

entries_router = APIRouter(
    prefix="/entries"
)

@entries_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_by_user(user_id: int, session: SessionDep):
    user_entry = await EntriesService.get_by_user(user_id, session)

    return user_entry

@entries_router.get("/today/{user_id}", status_code=status.HTTP_200_OK)
async def get_today_entry(user_id: int, session: SessionDep) -> Optional[SDailyEntry]:
    """
    Получить запись пользователя за сегодня.
    Возвращает null если записи за сегодня нет.
    """
    entry = await EntriesService.get_today_entry(user_id, session)
    return entry

@entries_router.post("", response_model=SDailyEntry, status_code=status.HTTP_201_CREATED)
async def add_entry(entry: SDailyEntryAdd, session: SessionDep):
    created_entry = await EntriesService.create(entry, session)

    return created_entry

@entries_router.put("/{entry_id}", response_model=SDailyEntry, status_code=status.HTTP_200_OK)
async def update_entry(entry_id: int, entry_data: SDailyEntryAdd, session: SessionDep):
    """Обновить существующую запись."""
    updated_entry = await EntriesService.update(entry_id, entry_data, session)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return updated_entry

