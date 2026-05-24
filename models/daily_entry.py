from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from datetime import date, datetime
from typing import Optional

from core.database import Model


class DailyEntryModel(Model):
    __tablename__ = "daily_entries"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date]
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    sleep: Mapped[Optional[int]] = mapped_column(default=None)
    energy: Mapped[Optional[int]] = mapped_column(default=None)
    clarity: Mapped[Optional[int]] = mapped_column(default=None)
    motivation: Mapped[Optional[int]] = mapped_column(default=None)
    tasks_planned: Mapped[Optional[str]] = mapped_column(default=None)
    tasks_done: Mapped[Optional[str]] = mapped_column(default=None)
    reflection: Mapped[Optional[str]] = mapped_column(default=None)
