from config.settings import dp, bot
from handlers import commands
import logging
from aiohttp import web
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.types import BotCommand
import os
from utils.middleware import LoggingMiddleware

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)
dp.message.middleware(LoggingMiddleware())

# Configura o webhook
async def on_startup(app):
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await bot.set_webhook(webhook_url)
    await set_bot_commands()
    logging.info(f"Webhook configurado em: {webhook_url}")

# Inicializa o aplicativo webhook
app = get_new_configured_app(dp, path="/webhook", bot=bot)
app.on_startup.append(on_startup)

# Ponto de entrada para o Render
if __name__ == "__main__":
    dp.include_router(commands.router)  # Inclui os roteadores

    # Se estiver em desenvolvimento local, use polling (para testes)
    if os.getenv("ENV") == "dev":
        logging.info("Modo: Polling (local)")
        from aiogram import executor
        executor.start_polling(dp, skip_updates=True)
    else:
        # Modo produção (Render)
        logging.info("Modo: Webhook (Render)")
        web.run_app(app, host="0.0.0.0", port=10000)
