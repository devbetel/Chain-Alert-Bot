from aiogram import BaseMiddleware
from config.settings import dp
import logging
from typing import Callable, Awaitable, Any
from aiogram.types import Message, TelegramObject

class LoggingMiddleware(BaseMiddleware): 

    async  def  __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        if isinstance(event, Message):
            logging.info(f"Recebido: {event.text}")
        
        try: 
            result = await handler(event, data)
            return result
        except Exception as e:
            logging.error(f"Erro no handler: {e}", exc_info=True)
            raise e