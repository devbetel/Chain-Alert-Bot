from config.settings import dp, bot
from handlers import commands
import asyncio
import logging
from utils.middleware import LoggingMiddleware


logging.basicConfig(level= logging.DEBUG)# Configura o nível de log para DEBUG


# dp.include_router(commands.router)
# dp.include_router(messages.router)
# dp.include_router(callbacks.router)
dp.message.middleware(LoggingMiddleware())  # Adiciona o middleware de logging



dp.include_router(commands.router)  # Inclui o roteador de comandos no dispatcher

async def main():
    await dp.start_polling(bot, skip_updates=True)  # Agora o bot é passado no start_polling

if __name__ == '__main__':
    print("Bot is polling...")

    asyncio.run(main())
