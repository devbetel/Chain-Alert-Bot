from aiogram.filters import CommandStart, Command
from aiogram import types, Router
from config.settings import dp  
from aiogram.types import Message, User, Chat
import requests
import requests_cache
from dotenv import load_dotenv
import os 
import datetime
load_dotenv()

requests_cache.install_cache('coingecko_cache', expire_after=3600)  # Cache de 1 hora
router = Router()
 

@router.message(CommandStart())
async def start(message: Message) -> None: 
    # Send a message when the command /start is issued
    await message.answer(f"Olá, {message.from_user.first_name}! Eu sou o ChainAlertBot. "
                        "Eu vou notificá-lo sobre as últimas notícias no mundo das criptomoedas. 🚀")

@router.message(Command("price"))
async def check_price(message: Message) -> None:
    try:
        # Extrai a moeda do comando (ex: /price bitcoin)
        coin = message.text.split()[1].lower().strip()
    except IndexError:
        await message.answer("❌ Por favor, informe uma moeda. Exemplo: <code>/price bitcoin</code>", parse_mode="HTML")
        return

    # Configura a URL da API (para moedas nativas como BTC, ETH, etc.)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true"
    headers = {"accept": "application/json", "x-cg-demo-api-key": os.getenv("API_KEY_COINGECKO")}


    try:
        await message.answer("🔄 Buscando o preço...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica erros HTTP
        data = response.json()
        print(f"Resposta veio do cache? {response.from_cache}")
        
        # Se a moeda não for encontrada 
        if not data or coin not in data:
            await message.answer(f"❌ Moeda <b>{coin}</b> não encontrada.", parse_mode="HTML")
            return

        # Pega preço e variação
        price = data[coin]["usd"]
        change = data[coin]["usd_24h_change"]

        # Formata a resposta
        await message.answer(
            f"💰 <b>{coin.upper()}</b>: ${price:,.2f}\n"
            f"📈 24h: {change:.2f}%",
            parse_mode="HTML"
        )

    except requests.exceptions.RequestException as e:
        await message.answer(f"⚠️ Erro na API: <code>{e}</code>", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"⚠️ Erro inesperado: <code>{e}</code>", parse_mode="HTML")

@router.message(Command("top10"))
async def top_coins(message: Message) -> None:  
    
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10"
    headers = {"accept": "application/json", "x-cg-demo-api-key": os.getenv("API_KEY_COINGECKO")}

    try:
        await message.answer("🔄 Buscando as 10 principais moedas...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica erros HTTP
        data = response.json()

        if not data:
            await message.answer("❌ Nenhuma moeda encontrada.")
            return
        
        # Formata a resposta
        await message.answer("\n".join(
            f"💰 <b>{coin['name']}</b>: ${coin['current_price']:,.2f} "
            f"(Variação 24h: {coin['price_change_percentage_24h']:.2f}%)"
            for coin in data
        ))
        
    except Exception as e:
        await message.answer(f"⚠️ Erro inesperado: <code>{e}</code>", parse_mode="HTML")
        return