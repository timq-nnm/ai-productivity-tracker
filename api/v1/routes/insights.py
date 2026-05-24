from fastapi import APIRouter, status
from typing import List

from schemas.insight import SInsight
from services.insights_service import InsightService
from core.database import SessionDep

insight_router = APIRouter(
    prefix="/insights"
)

@insight_router.get("/{user_id}", response_model=List[SInsight], status_code=status.HTTP_200_OK)
async def get_by_user(user_id: int, session: SessionDep):
    """
    Получить все инсайты пользователя.
    Каждый инсайт включает дату из связанной записи (entry_date).
    """
    insights = await InsightService.get_user_insights(user_id, session)
    
    # Преобразуем инсайты в формат с датой из связанной записи
    result = []
    for insight in insights:
        # _entry_date добавляется в InsightRepository через JOIN
        entry_date = getattr(insight, "_entry_date", None)
        insight_dict = {
            "id": insight.id,
            "user_id": insight.user_id,
            "period_type": insight.period_type,
            "summary": insight.summary,
            "recommendations": insight.recommendations,
            "mood": insight.mood,
            "productivity_score": insight.productivity_score,
            "created_at": insight.created_at,
            "entry_date": entry_date,
        }
        result.append(SInsight(**insight_dict))
    
    return result
