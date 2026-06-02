from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def admin_main_menu() -> ReplyKeyboardMarkup:
    """Admin main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kino qo'shish")],
            [KeyboardButton(text="🗑️ Kino o'chirish")],
            [KeyboardButton(text="🔍 Kino qidirish")],
            [KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📢 Broadcast yuborish")],
        ],
        resize_keyboard=True
    )
    return keyboard

def cancel_kb() -> ReplyKeyboardMarkup:
    """Cancel keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )
    return keyboard