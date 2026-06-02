from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_main_menu() -> ReplyKeyboardMarkup:
    """User main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Kino qidirish")],
        ],
        resize_keyboard=True
    )
    return keyboard