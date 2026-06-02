import os
from loguru import logger
import sys

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger.remove()  # Remove default handler

logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level=os.getenv('LOG_LEVEL', 'INFO')
)

logger.add(
    f"{log_dir}/bot.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="INFO",
    rotation="500 MB",
    retention="7 days"
)

__all__ = ["logger"]