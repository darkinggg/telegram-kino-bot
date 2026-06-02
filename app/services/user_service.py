from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import UserRepository
from app.models import User
from typing import Optional

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
    
    async def register_user(self, telegram_id: int, full_name: str, username: Optional[str] = None) -> User:
        """Register new user"""
        existing_user = await self.repo.get_by_telegram_id(telegram_id)
        if existing_user:
            return existing_user
        
        user_data = {
            "telegram_id": telegram_id,
            "full_name": full_name,
            "username": username
        }
        return await self.repo.create(user_data)
    
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram_id"""
        return await self.repo.get_by_telegram_id(telegram_id)
    
    async def get_total_users(self) -> int:
        """Get total users count"""
        return await self.repo.get_total_count()
    
    async def get_today_users(self) -> int:
        """Get today's new users count"""
        return await self.repo.get_today_count()