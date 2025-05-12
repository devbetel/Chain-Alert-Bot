from aiogram.filters import CommandStart, Command
from aiogram import Router
from config.settings import dp  
from aiogram.types import Message
import requests
from dotenv import load_dotenv

from requests_cache import CachedSession
import os 
import datetime
load_dotenv()

# 1. Cache para CoinGecko (1 hora)
coingecko_session = CachedSession(
    'coingecko_cache',
    expire_after=3600,
    backend='sqlite'
)

# 2. Cache para CryptoPanic (5 minutos)
cryptopanic_session = CachedSession(
    'news_cache',
    expire_after=300,
    backend='sqlite'
)


router = Router()
 
# Comando /start
# Inicia o bot e envia uma mensagem de boas-vindas
@router.message(CommandStart())
async def start(message: Message) -> None: 
    await message.answer(f"Olá, {message.from_user.first_name}! Eu sou o ChainAlertBot. "
                        "Eu vou notificá-lo sobre as últimas notícias no mundo das criptomoedas. 🚀")

# Comando /preço 
# Retorna o preço de uma moeda específica
@router.message(Command("preço"))
async def check_price(message: Message) -> None:
    try:
        # Extrai a moeda do comando (ex: /preço bitcoin)
        coin = message.text.split()[1].lower().strip()
    except IndexError:
        await message.answer("❌ Por favor, informe uma moeda. Exemplo: <code>/preço bitcoin</code>", parse_mode="HTML")
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

# Comando /top10
# Retorna as 10 principais moedas por capitalização de mercado
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
    
    
# Comando /ath
# Retorna o preço mais alto de todos os tempos (ATH) de uma moeda específica
@router.message(Command("ath"))
async def ath(message: Message) -> None:
    try:
        # Extrai a moeda do comando (ex: /ath bitcoin)
        coin = message.text.split()[1].lower().strip()
    except IndexError:
        await message.answer("❌ Por favor, informe uma moeda. Exemplo: <code>/ath bitcoin</code>", parse_mode="HTML")
        return
    # Configura a URL da API (para moedas nativas como BTC, ETH, etc.)
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"
    headers = {"accept": "application/json", "x-cg-demo-api-key": os.getenv("API_KEY_COINGECKO")}

    try: 
        await message.answer("🔄 Buscando o ATH...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica erros HTTP
        data = response.json()
        
        # Verifica se a moeda existe
        if not data:
            await message.answer(f"❌ Moeda <b>{coin}</b> não encontrada.", parse_mode="HTML")
            return
            
        # Pega o primeiro item da lista (que contém os dados da moeda)
        coin_data = data[0]
        ath_value = coin_data["ath"]
        ath_date = coin_data["ath_date"]
        ath_change = coin_data["ath_change_percentage"]
        
        # Formata a data
        ath_date = datetime.datetime.strptime(ath_date, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        ath_date = ath_date.strftime("%d/%m/%Y")  # Formata para DD/MM/YYYY

        # Formata a resposta
        await message.answer(
            f"🚀 <b>{coin.upper()} (ATH)</b>\n"
            f"💰 Preço: <b>${ath_value:,.2f}</b> (<b>{ath_date})</b>\n"
            f"⬇️ Desde o ATH: {ath_change:.2f}%\n",
            parse_mode="HTML"
        )

    except requests.exceptions.RequestException as e:
        await message.answer(f"⚠️ Erro na API: <code>{e}</code>", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"⚠️ Erro inesperado: <code>{e}</code>", parse_mode="HTML")

# Comando /fear
# Retorna o índice de medo e ganância do mercado
@router.message(Command("medo"))
async def fear_and_greed(message: Message) -> None:
    try:
        await message.answer("🔄 Buscando o índice de medo e ganância...")
        # Configura a URL da API da alternative.me
        response = requests.get("https://api.alternative.me/fng/")
        data= response.json()
        
        # pegando valores da API
        value = data["data"][0]["value"]
        classification = data["data"][0]["value_classification"]
        
        # Formata a resposta
        await message.answer(
            f"📊 <b>Fear & Greed Index</b>\n"
            f"🔢 Pontuação: <b>{value}</b> ({classification})\n"
            f"➡️ 0-49 = Medo | 50-100 = Ganância",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"⚠️ Erro ao acessar o índice: {e}")

# Comando /noticias
# Retorna as últimas notícias sobre criptomoedas        
@router.message(Command("noticias"))
async def news(message: Message) -> None:
    try: 
        await message.answer("🔄 Buscando notícias...")

        # Configura a URL da API
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={os.getenv('API_KEY_CRYPTOPANIC')}&currencies=BTC,ETH&kind=news"        


        # Faz a requisição
        response = requests.get(url)
        data = response.json()
        
        # Verifica se há dados
        if not data.get("results"):
            await message.answer("❌ Nenhuma notícia encontrada.")
            return
        
        # Pega a primeira notícia
        news_list = data["results"][:5]
        response_text = "📰 <b>Últimas Notícias (BTC/ETH)</b>\n\n"
       

        for i, news_item in enumerate(news_list, 1):
            # Pega os dados da notícia
            title= news_item.get("title", "Sem título")
            url = news_item.get("url", "#")
            source = news_item.get("source", {}).get("title", "Desconhecido")
            
            # Formata a data
            response_text += (
                f"{i}. <a href='{url}'>{title}</a>\n"
                f"   🗞️ <i>{source}</i>\n\n"
            )

        # Envia a resposta
        await message.answer(response_text, parse_mode="HTML")
        
    except requests.exceptions.RequestException as e:
        await message.answer(f"⚠️ Erro na API: <code>{e}</code>", parse_mode="HTML")

user_alerts = {}  # Dicionário para armazenar os alertas dos usuários
@router.message(Command("alerta"))
async def alert(message: Message) -> None:
    try:
        # Exemplo de comando: /alerta bitcoin 30000 mais
        parts = message.text.strip().split()
        if len(parts) != 4:
            await message.answer(
                "❌ Formato inválido. Use: /alerta <moeda> <valor> <mais|menor>\n"
                "Exemplo: /alerta bitcoin 30000 mais"
            )
            return

        coin = parts[1].lower()
        value = float(parts[2])
        direction = parts[3].lower()

        if direction not in ("mais", "menor"):
            await message.answer("❌ A direção deve ser 'mais' ou 'menor'.")
            return

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        headers = {"accept": "application/json", "x-cg-demo-api-key": os.getenv("API_KEY_COINGECKO")}
        await message.answer("🔄 Buscando o preço atual...")
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        
        if coin not in data:
            await message.answer(f"❌ Moeda <b>{coin}</b> não encontrada.", parse_mode="HTML")
            return

        current_price = data[coin]['usd']
        await message.answer(
            f"🔔 Alerta configurado para <b>{coin}</b> a <b>${value}</b> ({direction}).\n"
            f"Preço atual: <b>${current_price}</b>",
            parse_mode="HTML"
        )

        # Salvar o alerta
        user_id = message.from_user.id
        user_alerts.setdefault(user_id, []).append((coin, value, direction))

    except ValueError:
        await message.answer("❌ Valor inválido. Certifique-se de usar um número, por exemplo: 30000")
    except Exception as e:
        await message.answer(f"⚠️ Erro ao configurar alerta: {str(e)}")
        
@router.message(Command("ajuda"))
async def help(message: Message) -> None:

    await message.answer(
        "🤖 Olá! Eu sou o ChainAlertBot. Aqui estão os comandos que você pode usar:\n\n"
        "<b>/start</b> - Inicia o bot e mostra uma mensagem de boas-vindas\n\n"
        "<b>/preço [moeda]</b> - Verifica o preço atual de uma moeda (ex: /preço bitcoin)\n"
        "<b>/top10</b> - Mostra as 10 principais moedas por capitalização de mercado\n"
        "<b>/ath [moeda]</b> - Verifica o preço mais alto de todos os tempos (ATH) de uma moeda (ex: /ath bitcoin)\n"
        "<b>/medo</b> - Mostra o índice de medo e ganância do mercado\n"
        "<b>/noticias</b> - Mostra as últimas notícias sobre criptomoedas\n"
        "<b>/alerta [moeda] [valor] [mais|menor]</b> - Configura um alerta para uma moeda\n  "
        "<b>/ajuda</b> - Mostra esta mensagem de ajuda\n"
    )
    
@router.message()  # Sem filtros = captura qualquer mensagem
async def handle_unknown(message: Message):
    await message.answer("🤖 Comando não reconhecido. Tente novamente um comando reconhecido!")
    

