from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model
    
    async def create(self, obj_in: dict) -> T:
        """Create new object"""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, obj_id: int) -> Optional[T]:
        """Get object by ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()
    
    async def get_all(self) -> List[T]:
        """Get all objects"""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
    
    async def update(self, obj_id: int, obj_in: dict) -> Optional[T]:
        """Update object"""
        db_obj = await self.get_by_id(obj_id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            await self.session.commit()
            await self.session.refresh(db_obj)
        return db_obj
    
    async def delete(self, obj_id: int) -> bool:
        """Delete object"""
        db_obj = await self.get_by_id(obj_id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.commit()
            return True
        return False