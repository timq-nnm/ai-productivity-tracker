from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class SUserBase(BaseModel):
    username: str
    created_at: Optional[datetime] = None


class SUserAdd(SUserBase):
    pass


class SUser(SUserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
