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

@router.message(F.text == "🗑️ Kino o'chirish", AdminFilter())
async def delete_movie_start(message: Message, state: FSMContext):
    """Start deleting movie"""
    try:
        await message.answer(
            "🗑️ O'chiriladigan kinoning ID sini kiriting:",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_code_to_delete)
    except Exception as e:
        logger.error(f"Error in delete_movie_start: {e}")
        await message.answer("❌ Xatolik yuz berdi!")

@router.message(AdminStates.waiting_for_code_to_delete, F.text.isdigit(), AdminFilter())
async def delete_movie_confirm(message: Message, state: FSMContext, session: AsyncSession):
    """Delete movie"""
    try:
        movie_id = int(message.text)
        movie_service = MovieService(session)
        
        result = await movie_service.delete_movie(movie_id)
        
        if result:
            await message.answer(f"✅ Kino o'chirildi (ID: {movie_id})", reply_markup=admin_main_menu())
            logger.info(f"Admin {message.from_user.id} deleted movie {movie_id}")
        else:
            await message.answer("❌ Kino topilmadi!", reply_markup=admin_main_menu())
        
        await state.clear()
    except Exception as e:
        logger.error(f"Error deleting movie: {e}")
        await message.answer("❌ Xatolik yuz berdi!")

@router.message(F.text == "❌ Bekor qilish", AdminStates.waiting_for_code_to_delete, AdminFilter())
async def cancel_delete_movie(message: Message, state: FSMContext):
    """Cancel deleting movie"""
    try:
        await message.answer("❌ Bekor qilindi", reply_markup=admin_main_menu())
        await state.clear()
    except Exception as e:
        logger.error(f"Error in cancel_delete_movie: {e}")