from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.filters import AdminFilter
from app.services import MovieService
from app.states import AdminStates
from app.keyboards import admin_main_menu, cancel_kb
from app.utils import logger

router = Router()

@router.message(F.text == "➕ Kino qo'shish", AdminFilter())
async def add_movie_start(message: Message, state: FSMContext):
    """Kino qo'shishni boshlash"""
    try:
        await message.answer(
            "📹 Video yuborish:\n\n"
            "(Videoni faylni sifatida jo'natish kerak, rasm bo'lmay)",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_movie)
    except Exception as e:
        logger.error(f"Error in add_movie_start: {e}")
        await message.answer("❌ Xatolik yuz berdi!")

@router.message(AdminStates.waiting_for_movie, F.video, AdminFilter())
async def add_movie_video(message: Message, state: FSMContext, session: AsyncSession):
    """Video yuklanish"""
    try:
        if not message.video:
            await message.answer("❌ Video faylni yuborishingiz kerak!")
            return
        
        file_id = message.video.file_id
        movie_service = MovieService(session)
        
        # Kino qo'shish
        movie = await movie_service.add_movie(file_id)
        
        response_text = (
            "✅ Kino muvaffaqiyatli yuklandi!\n\n"
            f"🎬 Kino kodi: <b>{movie.code}</b>\n"
            f"📌 Foydalanuvchilar bu kodni kiritib kinoni ko'rishlari mumkin\n\n"
            f"ID: {movie.id}"
        )
        
        await message.answer(response_text, reply_markup=admin_main_menu(), parse_mode="HTML")
        logger.info(f"Admin {message.from_user.id} added movie {movie.id} with code {movie.code}")
        await state.clear()
    except Exception as e:
        logger.error(f"Error adding movie: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
        await state.clear()

@router.message(F.text == "❌ Bekor qilish", AdminStates.waiting_for_movie, AdminFilter())
async def cancel_add_movie(message: Message, state: FSMContext):
    """Kino qo'shishni bekor qilish"""
    try:
        await message.answer("❌ Bekor qilindi", reply_markup=admin_main_menu())
        await state.clear()
    except Exception as e:
        logger.error(f"Error in cancel_add_movie: {e}")