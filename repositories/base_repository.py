from typing import ClassVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

class BaseRepository:
    model: ClassVar[type[DeclarativeBase]]

    @classmethod
    async def get_one(cls, obj_id: int, session: AsyncSession):
        query = select(cls.model).where(cls.model.id == obj_id)  # type: ignore[attr-defined]

        result = await session.execute(query)

        return result.scalar_one_or_none()
    
    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)

        result = await session.execute(query)

        return list(result.scalars().all())

    @classmethod
    async def add_one(cls, data: dict, session: AsyncSession):
        obj = cls.model(**data)

        session.add(obj)

        await session.commit()
        await session.refresh(obj)

        return obj
    
    @classmethod
    async def update_one(cls, obj_id: int, data: dict, session: AsyncSession):
        obj = await cls.get_one(obj_id, session)

        if not obj:
            return None
        
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        await session.commit()
        await session.refresh(obj)

        return obj

    @classmethod
    async def delete_one(cls, obj_id: int, session: AsyncSession):
        obj = await cls.get_one(obj_id, session)

        if not obj:
            return None
        
        await session.delete(obj)
        await session.commit()

        return obj