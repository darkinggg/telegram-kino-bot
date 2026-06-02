from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from app.utils import logger


class LoggingMiddleware(BaseMiddleware):
    """Logging middleware"""
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            logger.info(f"Message from {event.from_user.id}: {event.text}")
        return await handler(event, data)