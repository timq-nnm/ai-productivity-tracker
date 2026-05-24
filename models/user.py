from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from core.database import Model


class UserModel(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str]
    created_at: Mapped[datetime]
