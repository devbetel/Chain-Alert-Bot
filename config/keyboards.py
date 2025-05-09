from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💰 Preços", callback_data="prices"))
    keyboard.add(InlineKeyboardButton("🔔 Alertas", callback_data="alerts"))
    return keyboard