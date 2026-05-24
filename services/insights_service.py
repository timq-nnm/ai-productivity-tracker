"""
Service для работы с инсайтами.
Использует LangGraph workflow для orchestration LLM pipeline.
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models.daily_entry import DailyEntryModel
from repositories.insight_repository import InsightRepository
from llm.graph.workflow import InsightWorkflow

logger = logging.getLogger(__name__)

# Singleton workflow instance
_workflow = InsightWorkflow()


class InsightService:
    @staticmethod
    async def generate(entry: DailyEntryModel, session: AsyncSession):
        """
        Сгенерировать инсайт через LangGraph workflow.
        
        Pipeline: validate → parse → analysis → save
        """
        entry_data = {
            "date": str(entry.date),
            "sleep": entry.sleep,
            "energy": entry.energy,
            "clarity": entry.clarity,
            "motivation": entry.motivation,
            "tasks_planned": entry.tasks_planned,
            "tasks_done": entry.tasks_done,
            "reflection": entry.reflection,
        }

        # Запускаем LangGraph workflow
        result = await _workflow.run(
            entry_data=entry_data,
            user_id=entry.user_id,
            entry_id=entry.id,
        )

        if result.get("error") or not result.get("insight"):
            logger.warning(f"Workflow failed for entry {entry.id}: {result.get('error')}")
            return None

        from llm.schemas.insight import DailyInsightSchema
        raw_insight = result["insight"]
        assert isinstance(raw_insight, DailyInsightSchema)
        insight_data = raw_insight

        # Сохраняем инсайт в БД
        insight = await InsightRepository.add_one(
            data={
                "user_id": entry.user_id,
                "entry_id": entry.id,
                "period_type": "daily",
                "summary": insight_data.summary,
                "recommendations": "\n".join(insight_data.recommendations),
                "mood": insight_data.mood,
                "productivity_score": insight_data.productivity_score,
                "created_at": entry.created_at,
            },
            session=session
        )

        logger.info(f"Insight saved for entry {entry.id}: mood={insight_data.mood}")
        return insight

    @staticmethod
    async def get_user_insights(user_id: int, session: AsyncSession):
        """Получить все инсайты пользователя."""
        return await InsightRepository.get_by_user(user_id, session)
