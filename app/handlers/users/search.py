from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import MovieService
from app.keyboards import user_main_menu, admin_main_menu
from app.utils import logger
from app.filters import AdminFilter

router = Router()

@router.message(F.text, ~F.text.startswith("/"))
async def search_movie(message: Message, session: AsyncSession, admin_filter: AdminFilter = None):
    """Kino kodini qidirish - admin va user uchun"""
    try:
        code = message.text.strip()
        
        # Kod uzunligini tekshirish
        if not code.isdigit() or len(code) != 3:
            await message.answer(
                "❌ Kino kodini noto'g'ri kiritdingiz!\n\n"
                "3 xonali raqamni kiritish kerak. Misol: 123",
                reply_markup=user_main_menu()
            )
            return
        
        movie_service = MovieService(session)
        movie = await movie_service.get_movie_by_code(code)
        
        if not movie:
            await message.answer(
                f"❌ Kod {code} topilmadi!\n\n"
                "Boshqa kod kiritib ko'ring",
                reply_markup=user_main_menu()
            )
            logger.warning(f"User {message.from_user.id} searched non-existent code {code}")
            return
        
        # Kino yuborish
        await message.answer_video(
            video=movie.file_id,
            caption=f"🎬 Kino (Kod: {movie.code})"
        )
        logger.info(f"User {message.from_user.id} watched movie {movie.id}")
        
    except Exception as e:
        logger.error(f"Error in search_movie: {e}")
        await message.answer(
            "❌ Xatolik yuz berdi!",
            reply_markup=user_main_menu()
        )