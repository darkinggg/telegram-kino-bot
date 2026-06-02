from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimitMiddleware(BaseMiddleware):
    """Rate limit middleware"""
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            user_id = event.from_user.id
            now = datetime.now()
            
            # Clean old requests
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if now - req_time < timedelta(seconds=self.time_window)
            ]
            
            # Check rate limit
            if len(self.requests[user_id]) >= self.max_requests:
                await event.answer("⏱️ Juda tez yozmoqdasiz. Ozgina kutib qoling!")
                return
            
            self.requests[user_id].append(now)
        
        return await handler(event, data)