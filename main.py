from config.settings import dp, bot
from handlers import commands
import logging
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from utils.middleware import LoggingMiddleware
from dotenv import load_dotenv

load_dotenv()

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
dp.message.middleware(LoggingMiddleware())

# Inclui os routers
dp.include_router(commands.router)

# Configurações do Webhook
WEBHOOK_PATH = "/webhook"
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").replace("https://", "").replace("http://", "")
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else None

async def on_startup(bot):
    if WEBHOOK_URL:
        logger.info(f"Configurando webhook em: {WEBHOOK_URL}")
        await bot.delete_webhook()  # Limpa webhook existente primeiro
        await bot.set_webhook(WEBHOOK_URL)
    else:
        logger.warning("WEBHOOK_URL não configurada - RENDER_EXTERNAL_HOSTNAME não definido")

# Cria o aplicativo aiohttp
app = web.Application()
app.on_startup.append(lambda app: on_startup(bot))

# Configura o webhook no aplicativo aiohttp
webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)
webhook_requests_handler.register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

if __name__ == "__main__":
    if not WEBHOOK_HOST or os.getenv("ENV") == "dev":
        logger.info("Modo: Polling (local)")
        import asyncio
        async def polling():
            await bot.delete_webhook()
            logger.info("Iniciando polling...")
            await dp.start_polling(bot)
        asyncio.run(polling())
    else:
        logger.info(f"Modo: Webhook (Render) - Host: {WEBHOOK_HOST}")
        web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", "10000")))