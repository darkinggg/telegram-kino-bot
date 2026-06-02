from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Movie
from .base import BaseRepository

class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Movie)
    
    async def get_by_code(self, code: str) -> Optional[Movie]:
        """Get movie by code"""
        result = await self.session.execute(
            select(Movie).where(Movie.code == code)
        )
        return result.scalars().first()
    
    async def code_exists(self, code: str) -> bool:
        """Check if code exists"""
        movie = await self.get_by_code(code)
        return movie is not None
    
    async def get_total_count(self) -> int:
        """Get total movies count"""
        result = await self.session.execute(select(Movie))
        return len(result.scalars().all())
    
    async def get_today_count(self) -> int:
        """Get today's added movies count"""
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        result = await self.session.execute(
            select(Movie).where(Movie.created_at >= today)
        )
        return len(result.scalars().all())