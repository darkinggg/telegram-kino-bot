from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.filters import AdminFilter
from app.keyboards import admin_main_menu
from app.utils import logger

router = Router()

@router.message(Command("start"), AdminFilter())
async def admin_start(message: Message):
    """Admin start"""
    try:
        admin_text = (
            "👨‍💼 Admin panelga xush kelibsiz!\n\n"
            "Pastdagi tugmalardan foydalaning:"
        )
        await message.answer(admin_text, reply_markup=admin_main_menu())
        logger.info(f"Admin {message.from_user.id} started")
    except Exception as e:
        logger.error(f"Error in admin start: {e}")
        await message.answer("❌ Xatolik yuz berdi!")