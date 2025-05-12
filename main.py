from config.settings import dp, bot
from handlers import commands
import logging
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from utils.middleware import LoggingMiddleware

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)
dp.message.middleware(LoggingMiddleware())

# Configurações do Webhook
WEBHOOK_PATH = f"/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

# Cria o aplicativo aiohttp
app = web.Application()
dp.include_router(commands.router)

# Configura o webhook no aplicativo aiohttp
webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)
webhook_requests_handler.register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

# Ponto de entrada para o Render
if __name__ == "__main__":
    if os.getenv("ENV") == "dev":
        logging.info("Modo: Polling (local)")
        import asyncio
        async def polling():
            await bot.delete_webhook()
            await dp.start_polling(bot)
        asyncio.run(polling())
    else:
        logging.info("Modo: Webhook (Render)")
        web.run_app(app, host="0.0.0.0", port=10000)
