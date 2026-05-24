"""
Analytics API endpoints — ЭТАП 6.

Endpoints:
- GET /analytics/burnout/{user_id}
- GET /analytics/trends/{user_id}
- GET /analytics/patterns/{user_id}
- GET /analytics/streak/{user_id}
"""
from fastapi import APIRouter, status

from core.database import SessionDep
from services.analytics_service import AnalyticsService

analytics_router = APIRouter(prefix="/analytics")


@analytics_router.get("/burnout/{user_id}", status_code=status.HTTP_200_OK)
async def get_burnout_risk(user_id: int, session: SessionDep):
    """
    Определить риск выгорания пользователя.
    
    Анализирует последние 7 дней и возвращает:
    - Уровень риска (none/low/medium/high/critical)
    - Метрики
    - Рекомендации
    """
    return await AnalyticsService.get_burnout_risk(user_id, session)


@analytics_router.get("/trends/{user_id}", status_code=status.HTTP_200_OK)
async def get_trends(user_id: int, session: SessionDep, days: int = 14):
    """
    Анализ трендов метрик за период.
    
    Возвращает направление тренда (rising/stable/falling)
    и процент изменения для sleep, energy, clarity, motivation.
    """
    return await AnalyticsService.get_trends(user_id, session, days=days)


@analytics_router.get("/patterns/{user_id}", status_code=status.HTTP_200_OK)
async def get_productivity_patterns(user_id: int, session: SessionDep):
    """
    Паттерны продуктивности по дням недели.
    
    Определяет лучшие и худшие дни недели за последние 30 дней.
    """
    return await AnalyticsService.get_productivity_patterns(user_id, session)


@analytics_router.get("/streak/{user_id}", status_code=status.HTTP_200_OK)
async def get_streak(user_id: int, session: SessionDep):
    """
    Streak — количество дней подряд с записями.
    """
    return await AnalyticsService.get_streak(user_id, session)
