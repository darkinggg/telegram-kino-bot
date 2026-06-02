from aiogram.filters import Filter
from aiogram.types import Message
import os

class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        admin_id = int(os.getenv('ADMIN_ID', 0))
        is_admin = message.from_user.id == admin_id
        return is_admin