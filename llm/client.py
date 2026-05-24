"""
LLM Client с поддержкой Structured Output через Pydantic.
Использует with_structured_output() для надёжного JSON парсинга.
"""
import logging
from typing import TypeVar, Type, cast

from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage

from config import GIGACHAT_API_KEY
from llm.schemas.insight import DailyInsightSchema, WeeklyInsightSchema, ParsedTaskSchema
from llm.prompts import (
    DAILY_INSIGHT_SYSTEM_PROMPT,
    DAILY_INSIGHT_USER_TEMPLATE,
    WEEKLY_INSIGHT_SYSTEM_PROMPT,
    WEEKLY_INSIGHT_USER_TEMPLATE,
    PARSE_TASKS_SYSTEM_PROMPT,
    PARSE_TASKS_USER_TEMPLATE,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class LLMClient:
    """
    GigaChat клиент с Structured Output.
    
    Использует with_structured_output() для получения валидных Pydantic объектов
    вместо ручного парсинга текста.
    """

    def __init__(self, model_name: str = "GigaChat-2"):
        self._base_model = GigaChat(
            credentials=GIGACHAT_API_KEY,
            model=model_name,
            verify_ssl_certs=False,
        )

    def _get_structured_model(self, schema: Type[T]):
        """Получить модель с привязанной Pydantic схемой."""
        return self._base_model.with_structured_output(schema)

    async def generate_daily_insight(self, entry_data: dict) -> DailyInsightSchema:
        """
        Генерировать инсайт для одного дня.
        Возвращает валидный DailyInsightSchema объект.
        """
        structured_llm = self._get_structured_model(DailyInsightSchema)

        user_message = DAILY_INSIGHT_USER_TEMPLATE.format(**entry_data)
        messages = [
            SystemMessage(content=DAILY_INSIGHT_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        try:
            raw = await structured_llm.ainvoke(messages)
            result = cast(DailyInsightSchema, raw)
            logger.info(f"Daily insight generated: mood={result.mood}, score={result.productivity_score}")
            return result
        except Exception as e:
            logger.error(f"Structured output failed: {e}, falling back to default")
            return self._default_daily_insight()

    async def generate_weekly_insight(self, stats: dict, daily_details: str) -> WeeklyInsightSchema:
        """
        Генерировать инсайт для недели.
        Возвращает валидный WeeklyInsightSchema объект.
        """
        structured_llm = self._get_structured_model(WeeklyInsightSchema)

        user_message = WEEKLY_INSIGHT_USER_TEMPLATE.format(
            days=stats.get("entries_count", 0),
            avg_sleep=stats.get("avg_sleep", 0),
            avg_energy=stats.get("avg_energy", 0),
            avg_clarity=stats.get("avg_clarity", 0),
            avg_motivation=stats.get("avg_motivation", 0),
            daily_details=daily_details,
        )
        messages = [
            SystemMessage(content=WEEKLY_INSIGHT_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        try:
            raw = await structured_llm.ainvoke(messages)
            result = cast(WeeklyInsightSchema, raw)
            logger.info("Weekly insight generated")
            return result
        except Exception as e:
            logger.error(f"Weekly insight failed: {e}")
            return self._default_weekly_insight()

    async def parse_tasks_from_text(self, text: str) -> ParsedTaskSchema:
        """
        Парсить задачи из свободного текста пользователя.
        Используется для обработки вечернего отчёта.
        """
        structured_llm = self._get_structured_model(ParsedTaskSchema)

        messages = [
            SystemMessage(content=PARSE_TASKS_SYSTEM_PROMPT),
            HumanMessage(content=PARSE_TASKS_USER_TEMPLATE.format(text=text)),
        ]

        try:
            raw = await structured_llm.ainvoke(messages)
            result = cast(ParsedTaskSchema, raw)
            return result
        except Exception as e:
            logger.error(f"Task parsing failed: {e}")
            return ParsedTaskSchema(
                tasks_completed=[text],
                distractions=[],
                physical_activity=False,
                social_interaction=False,
                mood_summary="Не удалось определить",
            )

    # ─── Fallback defaults ────────────────────────────────────────────────────

    def _default_daily_insight(self) -> DailyInsightSchema:
        return DailyInsightSchema(
            summary="Не удалось сгенерировать анализ. Попробуйте позже.",
            recommendations=["Продолжайте вести дневник для накопления данных"],
            mood="neutral",
            productivity_score=5,
            energy_trend="stable",
        )

    def _default_weekly_insight(self) -> WeeklyInsightSchema:
        return WeeklyInsightSchema(
            summary="Недостаточно данных для анализа недели.",
            patterns=[],
            recommendations=["Заполняйте дневник каждый день для лучшего анализа"],
            best_day="Нет данных",
            improvement_areas=[],
        )
