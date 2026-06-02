from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
import random
from app.models import Movie

class MovieService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_movie(self, file_id: str) -> Movie:
        """Kino qo'shish - random 3 xonali kod bilan"""
        # Random 3 xonali kod yaratish (100-999)
        while True:
            code = str(random.randint(100, 999))
            
            # Kod mavjud bo'lmasligini tekshirish
            stmt = select(Movie).where(Movie.code == code)
            result = await self.session.execute(stmt)
            if not result.scalars().first():
                break
        
        movie = Movie(
            code=code,
            file_id=file_id
        )
        self.session.add(movie)
        await self.session.commit()
        await self.session.refresh(movie)
        return movie
    
    async def delete_movie(self, movie_id: int) -> bool:
        """Kino o'chirish"""
        stmt = select(Movie).where(Movie.id == movie_id)
        result = await self.session.execute(stmt)
        movie = result.scalars().first()
        
        if movie:
            await self.session.delete(movie)
            await self.session.commit()
            return True
        return False
    
    async def get_movie_by_code(self, code: str) -> Movie:
        """Kod bo'yicha kino topish"""
        stmt = select(Movie).where(Movie.code == code)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_total_movies(self) -> int:
        """Jami kinolar"""
        stmt = select(func.count(Movie.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def get_today_movies(self) -> int:
        """Bugungi yangi kinolar"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(func.count(Movie.id)).where(Movie.created_at >= today)
        result = await self.session.execute(stmt)
        return result.scalar() or 0