from fastapi import APIRouter, status

from schemas.user import SUser, SUserAdd
from core.database import SessionDep
from services.users_service import UsersService

users_router = APIRouter(
    prefix="/users"
)

@users_router.get("", response_model=list[SUser], status_code=status.HTTP_200_OK)
async def get_all_users(session: SessionDep):
    return await UsersService.get_all_users(session)

@users_router.get("/by-username/{username}", response_model=SUser, status_code=status.HTTP_200_OK)
async def get_by_username(username: str, session: SessionDep):
    return await UsersService.get_by_username(username, session)

@users_router.get("/{user_id}", response_model=SUser, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: SessionDep):
    return await UsersService.get_user(user_id, session)

@users_router.post("", response_model=SUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: SUserAdd, session: SessionDep):
    return await UsersService.create_user(user, session)

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep):
    return await UsersService.delete_user(user_id, session)
