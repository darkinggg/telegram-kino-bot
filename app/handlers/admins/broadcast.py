from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.filters import AdminFilter
from app.models import User
from app.states import AdminStates
from app.keyboards import admin_main_menu, cancel_kb
from app.utils import logger

router = Router()

@router.message(F.text == "📢 Broadcast yuborish", AdminFilter())
async def broadcast_start(message: Message, state: FSMContext):
    """Start broadcast"""
    try:
        await message.answer(
            "📢 Barcha foydalanuvchilarga yuboriladi xabar:\n\n"
            "Xabar matnini kiriting:",
            reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.waiting_for_broadcast_message)
    except Exception as e:
        logger.error(f"Error in broadcast_start: {e}")
        await message.answer("❌ Xatolik yuz berdi!")

@router.message(AdminStates.waiting_for_broadcast_message, AdminFilter())
async def broadcast_send(message: Message, state: FSMContext, session: AsyncSession, bot):
    """Send broadcast"""
    try:
        broadcast_text = message.text
        
        # Get all users
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        sent = 0
        failed = 0
        
        for user in users:
            try:
                await bot.send_message(user.telegram_id, broadcast_text)
                sent += 1
            except Exception as e:
                logger.warning(f"Failed to send message to {user.telegram_id}: {e}")
                failed += 1
        
        report_text = (
            f"✅ Broadcast yakunlandi!\n\n"
            f"📤 Yuborildi: {sent}\n"
            f"❌ Xatolik: {failed}"
        )
        
        await message.answer(report_text, reply_markup=admin_main_menu())
        logger.info(f"Admin {message.from_user.id} sent broadcast to {sent} users")
        await state.clear()
    except Exception as e:
        logger.error(f"Error in broadcast: {e}")
        await message.answer("❌ Xatolik yuz berdi!")

@router.message(F.text == "❌ Bekor qilish", AdminStates.waiting_for_broadcast_message, AdminFilter())
async def cancel_broadcast(message: Message, state: FSMContext):
    """Cancel broadcast"""
    try:
        await message.answer("❌ Bekor qilindi", reply_markup=admin_main_menu())
        await state.clear()
    except Exception as e:
        logger.error(f"Error in cancel_broadcast: {e}")