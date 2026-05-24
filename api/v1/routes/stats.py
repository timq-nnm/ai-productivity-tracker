from fastapi import APIRouter, status, HTTPException

from schemas.stat import SWeeklyStats
from services.stats_service import StatsService
from core.database import SessionDep

stats_router = APIRouter(
    prefix="/stats"
)

@stats_router.get("/week/{user_id}", response_model=SWeeklyStats)
async def get_week_stats(user_id: int, session: SessionDep):
    return await StatsService.get_week_stats(user_id, session)