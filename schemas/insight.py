from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime

class SInsightBase(BaseModel):
    period_type: str
    summary: str
    recommendations: str
    mood: str | None = None
    productivity_score: int | None = None
    entry_date: date | None = None  # Дата из связанной записи

    created_at: datetime

class SInsightAdd(SInsightBase):
    user_id: int

class SInsight(SInsightBase):
    id: int
    user_id: int | None = None

    model_config = ConfigDict(from_attributes=True)