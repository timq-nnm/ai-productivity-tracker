from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime

class SDailyEntryBase(BaseModel):
    date: date
    created_at: datetime | None = None

    sleep: int | None = Field(default=None, ge=0, le=10)
    energy: int | None = Field(default=None, ge=0, le=10)
    clarity: int | None = Field(default=None, ge=0, le=10)
    motivation: int | None = Field(default=None, ge=0, le=10)
    tasks_planned: str | None = None
    tasks_done: str | None = None
    reflection: str | None = None

class SDailyEntryAdd(SDailyEntryBase):
    user_id: int
    date: date

class SDailyEntry(SDailyEntryBase):
    id: int
    user_id: int | None = None

    model_config = ConfigDict(from_attributes=True)