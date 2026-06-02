from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.filters import AdminFilter
from app.services import UserService, MovieService
from app.keyboards import admin_main_menu
from app.utils import logger

router = Router()

@router.message(F.text == "📊 Statistika", AdminFilter())
async def show_stats(message: Message, session: AsyncSession):
    """Admin statistikani ko'rish"""
    try:
        user_service = UserService(session)
        movie_service = MovieService(session)
        
        total_users = await user_service.get_total_users()
        total_movies = await movie_service.get_total_movies()
        today_users = await user_service.get_today_users()
        today_movies = await movie_service.get_today_movies()
        
        stats_text = (
            "📊 STATISTIKA\n\n"
            f"👥 Jami foydalanuvchilar: {total_users}\n"
            f"📅 Bugungi foydalanuvchilar: {today_users}\n\n"
            f"🎬 Jami kinolar: {total_movies}\n"
            f"📅 Bugungi kinolar: {today_movies}"
        )
        
        await message.answer(stats_text, reply_markup=admin_main_menu())
        logger.info(f"Admin {message.from_user.id} viewed stats")
    except Exception as e:
        logger.error(f"Error showing stats: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}", reply_markup=admin_main_menu())