from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter  # Yangi qo'shildi
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
            "(Videoni faylni sifatida jo'natish kerak)",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_movie)
    except Exception as e:
        logger.error(f"Error in add_movie_start: {e}")
        await message.answer("❌ Xatolik yuz berdi!")

@router.message(AdminStates.waiting_for_movie, F.video, AdminFilter())
async def add_movie_video(message: Message, state: FSMContext):
    """Video yuklanish"""
    try:
        if not message.video:
            await message.answer("❌ Video faylni yuborishingiz kerak!")
            return
        
        file_id = message.video.file_id
        await state.update_data(file_id=file_id)
        
        await message.answer(
            "📝 Kino nomini kiriting:",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_movie_title)
    except Exception as e:
        logger.error(f"Error adding movie: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
        await state.clear()

@router.message(AdminStates.waiting_for_movie_title, F.text, AdminFilter())
async def add_movie_title(message: Message, state: FSMContext):
    """Kino nomi"""
    try:
        await state.update_data(title=message.text)
        
        await message.answer(
            "👤 Rejissyorni kiriting:",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_movie_director)
    except Exception as e:
        logger.error(f"Error: {e}")

@router.message(AdminStates.waiting_for_movie_director, F.text, AdminFilter())
async def add_movie_director(message: Message, state: FSMContext):
    """Kino rejissyori"""
    try:
        await state.update_data(director=message.text)
        
        await message.answer(
            "📅 Yilni kiriting:",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_movie_year)
    except Exception as e:
        logger.error(f"Error: {e}")

@router.message(AdminStates.waiting_for_movie_year, F.text, AdminFilter())
async def add_movie_year(message: Message, state: FSMContext):
    """Kino yili"""
    try:
        await state.update_data(year=int(message.text))
        
        categories = ["Drama", "Komediya", "Aksyon", "Thriller", "Sevgi", "Qo'rquv", "Fantastika", "Multfilm"]
        keyboard_text = "\n".join([f"{i+1}. {cat}" for i, cat in enumerate(categories)])
        
        await message.answer(
            f"📂 Kategoriyani tanlang:\n\n{keyboard_text}\n\n(Raqam yuboring)",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_movie_category)
    except Exception as e:
        logger.error(f"Error: {e}")

@router.message(AdminStates.waiting_for_movie_category, F.text, AdminFilter())
async def add_movie_category(message: Message, state: FSMContext):
    """Kino kategoriyasi"""
    try:
        categories = ["Drama", "Komediya", "Aksyon", "Thriller", "Sevgi", "Qo'rquv", "Fantastika", "Multfilm"]
        idx = int(message.text) - 1
        
        if 0 <= idx < len(categories):
            await state.update_data(category=categories[idx])
            
            await message.answer(
                "📖 Tavsifni kiriting:",
                reply_markup=cancel_kb()
            )
            await state.set_state(AdminStates.waiting_for_movie_description)
        else:
            await message.answer("❌ Noto'g'ri raqam!")
    except Exception as e:
        logger.error(f"Error: {e}")

@router.message(AdminStates.waiting_for_movie_description, F.text, AdminFilter())
async def add_movie_description(message: Message, state: FSMContext, session: AsyncSession):
    """Kino tavsifi va saqlash"""
    try:
        data = await state.get_data()
        
        movie_service = MovieService(session)
        movie = await movie_service.add_movie(
            file_id=data['file_id'],
            title=data['title'],
            director=data['director'],
            year=data['year'],
            category=data['category'],
            description=message.text
        )
        
        response_text = (
            "✅ Kino muvaffaqiyatli yuklandi!\n\n"
            f"🎬 Nomi: {movie.title}\n"
            f"👤 Rejissyori: {movie.director}\n"
            f"📅 Yili: {movie.year}\n"
            f"📂 Kategoriyasi: {movie.category}\n"
            f"🔑 Kino kodi: <b>{movie.code}</b>"
        )
        
        await message.answer(response_text, reply_markup=admin_main_menu(), parse_mode="HTML")
        logger.info(f"Admin {message.from_user.id} added movie {movie.id}")
        await state.clear()
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
        await state.clear()

# Bu yerda | operatori o'rniga StateFilter ishlatildi:
@router.message(
    F.text == "❌ Bekor qilish", 
    StateFilter(
        AdminStates.waiting_for_movie_title, 
        AdminStates.waiting_for_movie_director, 
        AdminStates.waiting_for_movie_year, 
        AdminStates.waiting_for_movie_category, 
        AdminStates.waiting_for_movie_description
    ), 
    AdminFilter()
)
async def cancel_add_movie(message: Message, state: FSMContext):
    """Kino qo'shishni bekor qilish"""
    try:
        await message.answer("❌ Bekor qilindi", reply_markup=admin_main_menu())
        await state.clear()
    except Exception as e:
        logger.error(f"Error: {e}")