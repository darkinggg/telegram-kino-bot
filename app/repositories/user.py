from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from .base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram_id"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()
    
    async def get_total_count(self) -> int:
        """Get total users count"""
        result = await self.session.execute(select(User))
        return len(result.scalars().all())
    
    async def get_today_count(self) -> int:
        """Get today's joined users count"""
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        result = await self.session.execute(
            select(User).where(User.joined_at >= today)
        )
        return len(result.scalars().all())