from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime
import random
from app.models import Movie, Category, UserMovie

class MovieService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_movie(self, file_id: str, title: str, director: str = None, 
                       year: int = None, category: str = None, 
                       description: str = None) -> Movie:
        """Kino qo'shish - barcha malumotlar bilan"""
        while True:
            code = str(random.randint(100, 999))
            stmt = select(Movie).where(Movie.code == code)
            result = await self.session.execute(stmt)
            if not result.scalars().first():
                break
        
        movie = Movie(
            code=code,
            file_id=file_id,
            title=title,
            director=director,
            year=year,
            category=category,
            description=description
        )
        self.session.add(movie)
        await self.session.commit()
        await self.session.refresh(movie)
        return movie
    
    async def get_movie_by_code(self, code: str) -> Movie:
        """Kod bo'yicha kino topish"""
        stmt = select(Movie).where(Movie.code == code)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def search_by_title(self, title: str) -> list:
        """Nomi bo'yicha qidiruv"""
        stmt = select(Movie).where(Movie.title.ilike(f"%{title}%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search_by_category(self, category: str) -> list:
        """Kategoriya bo'yicha qidiruv"""
        stmt = select(Movie).where(Movie.category == category)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_top_rated(self, limit: int = 5) -> list:
        """Eng yuqori reyting bo'lgan kinolar"""
        stmt = select(Movie).order_by(Movie.rating.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def rate_movie(self, movie_id: int, user_id: int, rating: int) -> Movie:
        """Kino reyting berish"""
        stmt = select(Movie).where(Movie.id == movie_id)
        result = await self.session.execute(stmt)
        movie = result.scalars().first()
        
        if movie:
            # Yangi o'rtacha rating hisoblash
            total = movie.rating * movie.total_ratings
            total += rating
            movie.total_ratings += 1
            movie.rating = total / movie.total_ratings
            
            await self.session.commit()
            await self.session.refresh(movie)
        
        return movie
    
    async def add_to_favorites(self, movie_id: int, user_id: int):
        """Sevimlilar ro'yxatiga qo'shish"""
        stmt = select(UserMovie).where(
            and_(
                UserMovie.movie_id == movie_id,
                UserMovie.user_id == user_id
            )
        )
        result = await self.session.execute(stmt)
        user_movie = result.scalars().first()
        
        if user_movie:
            user_movie.is_favorite = "yes"
        else:
            user_movie = UserMovie(
                user_id=user_id,
                movie_id=movie_id,
                is_favorite="yes"
            )
            self.session.add(user_movie)
        
        await self.session.commit()
        return user_movie
    
    async def get_favorites(self, user_id: int) -> list:
        """Foydalanuvchining sevimli kinolari"""
        stmt = select(UserMovie).where(
            and_(
                UserMovie.user_id == user_id,
                UserMovie.is_favorite == "yes"
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def add_comment(self, movie_id: int, user_id: int, comment: str, rating: int):
        """Kino uchun komment qo'shish"""
        stmt = select(UserMovie).where(
            and_(
                UserMovie.movie_id == movie_id,
                UserMovie.user_id == user_id
            )
        )
        result = await self.session.execute(stmt)
        user_movie = result.scalars().first()
        
        if not user_movie:
            user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
            self.session.add(user_movie)
        
        user_movie.comment = comment
        user_movie.rating = rating
        
        await self.session.commit()
        await self.session.refresh(user_movie)
        return user_movie
    
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