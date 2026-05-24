"""
State для LangGraph workflow.
Хранит данные между нодами графа.
"""
from typing import TypedDict, Optional
from llm.schemas.insight import DailyInsightSchema, ParsedTaskSchema


class InsightWorkflowState(TypedDict):
    """Состояние графа обработки daily entry."""

    # Входные данные
    user_id: int
    entry_id: int
    raw_entry: dict  # Сырые данные из БД

    # Промежуточные результаты
    parsed_tasks: Optional[ParsedTaskSchema]
    validation_passed: bool
    validation_errors: list[str]

    # Финальный результат
    insight: Optional[DailyInsightSchema]
    insight_saved: bool
    error: Optional[str]
