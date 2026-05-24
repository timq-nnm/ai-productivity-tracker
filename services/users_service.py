from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import SUserAdd
from repositories.user_repository import UsersRepository
from core.exceptions.users_exceptions import UserNotFoundError, UserAlreadyExsist

class UsersService:
    @staticmethod
    async def get_user(user_id: int, session: AsyncSession):
        user_model = await UsersRepository.get_one(user_id, session)

        if user_model is None:
            raise UserNotFoundError()

        return user_model
    
    @staticmethod
    async def get_by_username(username: str, session: AsyncSession):
        user_model = await UsersRepository.get_by_username(username, session)
        return user_model
    
    @staticmethod
    async def get_all_users(session: AsyncSession):
        user_model_list = await UsersRepository.get_all(session)

        return user_model_list
    
    @staticmethod
    async def create_user(user: SUserAdd, session: AsyncSession):
        from datetime import datetime, timezone
        # Проверяем по username
        existing_user = await UsersRepository.get_by_username(user.username, session)
        if existing_user:
            raise UserAlreadyExsist

        data = user.model_dump()
        if not data.get("created_at"):
            data["created_at"] = datetime.now(timezone.utc)
        user_model = await UsersRepository.add_one(data, session)

        return user_model
    
    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession):
        obj = await UsersRepository.delete_one(user_id, session)
            
        if not obj:
            raise UserNotFoundError()
        
        return None
