import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, AsyncSessionLocal
from app.models import User, Movie
from app.middlewares import LoggingMiddleware, RateLimitMiddleware
from app.handlers.users import routers as user_routers
from app.handlers.admins import routers as admin_routers
from app.utils import logger

load_dotenv()

# Bot va Dispatcher o'rnatish
BOT_TOKEN = os.getenv('BOT_TOKEN')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file!")

bot = Bot(token=BOT_TOKEN)
storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)

# Dependency injection uchun middleware
async def session_middleware(handler, event, data):
    async with AsyncSessionLocal() as session:
        data['session'] = session
        data['bot'] = bot
        return await handler(event, data)

# Middleware ro'yxati
dp.message.middleware(LoggingMiddleware())
dp.message.middleware(RateLimitMiddleware())

# Handler ro'yxati
dp.include_routers(*admin_routers, *user_routers) 

# Database va Bot Commands
async def setup_bot_commands():
    """Bot commands o'rnatish"""
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="stats", description="Statistikani ko'rish (Faqat Admin)"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def create_tables():
    """Database tables yaratish"""
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Movie.metadata.create_all)

async def main():
    """Bot ishga tushirish"""
    try:
        logger.info("Bot ishga tushyapti...")
        
        # Database setup
        await create_tables()
        logger.info("Database tables yaratildi/tekshirildi")
        
        # Bot commands
        await setup_bot_commands()
        logger.info("Bot commands o'rnatildi")
        
        # Session dependency
        from aiogram.types import Update
        from typing import Any, Callable, Dict, Awaitable
        from aiogram import BaseMiddleware
        
        class SessionMiddleware(BaseMiddleware):
            async def __call__(
                self,
                handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
                event: Update,
                data: Dict[str, Any],
            ) -> Any:
                async with AsyncSessionLocal() as session:
                    data['session'] = session
                    data['bot'] = bot
                    return await handler(event, data)
        
        dp.update.middleware(SessionMiddleware())
        
        # Bot ishga tushirish
        logger.info("Bot polling boshlanmoqda...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
    except Exception as e:
        logger.error(f"Bot xatosi: {e}")
    finally:
        await bot.session.close()
        await engine.dispose()
        logger.info("Bot to'xtatildi")

if __name__ == "__main__":
    asyncio.run(main())