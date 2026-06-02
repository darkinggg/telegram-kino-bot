from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime
from app.models import User, UserMovie

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def register_user(self, telegram_id: int, full_name: str, username: str = None) -> User:
        """Foydalanuvchini ro'yxatga olish"""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        
        if user:
            return user
        
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def add_to_watch_history(self, user_id: int, movie_id: int):
        """Ko'rish tarixiga qo'shish"""
        stmt = select(UserMovie).where(
            and_(
                UserMovie.user_id == user_id,
                UserMovie.movie_id == movie_id
            )
        )
        result = await self.session.execute(stmt)
        user_movie = result.scalars().first()
        
        if not user_movie:
            user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
            self.session.add(user_movie)
        
        user_movie.watched_at = datetime.utcnow()
        await self.session.commit()
    
    async def get_watch_history(self, user_id: int) -> list:
        """Ko'rish tarixi"""
        stmt = select(UserMovie).where(UserMovie.user_id == user_id).order_by(UserMovie.watched_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_total_users(self) -> int:
        """Jami foydalanuvchilar"""
        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def get_today_users(self) -> int:
        """Bugungi yangi foydalanuvchilar"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(func.count(User.id)).where(User.joined_at >= today)
        result = await self.session.execute(stmt)
        return result.scalar() or 0