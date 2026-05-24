"""
Pydantic схемы для Structured LLM Output.
Вместо парсинга текста — валидные JSON модели.
"""
from pydantic import BaseModel, Field
from typing import Literal


class DailyInsightSchema(BaseModel):
    """Структурированный инсайт от LLM для одного дня."""

    summary: str = Field(description="Краткий анализ дня в 1-2 предложениях")
    recommendations: list[str] = Field(
        description="Список рекомендаций на основе анализа",
        max_length=5,
    )
    mood: Literal["great", "good", "neutral", "low", "bad"] = Field(
        description="Общее настроение за день"
    )
    productivity_score: int = Field(
        ge=0, le=10, description="Оценка продуктивности 0-10"
    )
    energy_trend: Literal["rising", "stable", "falling"] = Field(
        description="Тренд энергии за день"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "summary": "Продуктивный день с хорошим уровнем энергии",
                "recommendations": [
                    "Продолжать утреннюю рутину",
                    "Увеличить время на физическую активность",
                ],
                "mood": "good",
                "productivity_score": 7,
                "energy_trend": "stable",
            }
        }
    }


class WeeklyInsightSchema(BaseModel):
    """Структурированный инсайт для недельного периода."""

    summary: str = Field(description="Общий анализ недели")
    patterns: list[str] = Field(
        description="Выявленные паттерны поведения",
        max_length=5,
    )
    recommendations: list[str] = Field(
        description="Рекомендации на следующую неделю",
        max_length=5,
    )
    best_day: str = Field(description="Самый продуктивный день недели")
    improvement_areas: list[str] = Field(
        description="Области для улучшения",
        max_length=3,
    )


class ParsedTaskSchema(BaseModel):
    """Распарсенные задачи из свободного текста (вечерний отчёт)."""

    tasks_completed: list[str] = Field(description="Выполненные задачи")
    distractions: list[str] = Field(description="Отвлечения/прокрастинация")
    physical_activity: bool = Field(description="Была ли физическая активность")
    social_interaction: bool = Field(description="Было ли социальное взаимодействие")
    mood_summary: str = Field(description="Краткое описание настроения")
