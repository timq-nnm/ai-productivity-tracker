from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime, date

from core.database import Model


class InsightModel(Model):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    period_type: Mapped[str]
    summary: Mapped[str]
    recommendations: Mapped[str]
    created_at: Mapped[datetime]

    # Опциональные поля — после обязательных
    entry_id: Mapped[int | None] = mapped_column(ForeignKey("daily_entries.id"), default=None)
    mood: Mapped[str | None] = mapped_column(default=None)
    productivity_score: Mapped[int | None] = mapped_column(default=None)
