from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import UserModel
from repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository):
    model = UserModel

    @classmethod
    async def get_by_username(cls, username: str, session: AsyncSession) -> UserModel | None:
        query = select(UserModel).where(UserModel.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()
