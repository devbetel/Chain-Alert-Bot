# 📈 ChainAlertBot - Bot de Criptomoedas para Telegram  

Um bot para Telegram que fornece informações sobre criptomoedas, incluindo preços, notícias, índices de mercado e alertas personalizados.  

---

## 🚀 **Funcionalidades**  

✅ **Preços em tempo real** (`/preço [moeda]`)  
✅ **Top 10 criptomoedas por capitalização** (`/top10`)  
✅ **Preço mais alto de todos os tempos (ATH)** (`/ath [moeda]`)  
✅ **Índice de Medo e Ganância** (`/medo`)  
✅ **Últimas notícias sobre criptomoedas** (`/noticias`)  
✅ **Alertas personalizados** (`/alerta [moeda] [valor] [mais|menor]`)  
✅ **Guia de comandos** (`/ajuda`)  

---

## ⚙️ **Tecnologias Utilizadas**  

- **Python 3.10+**  
- **Aiogram** (Biblioteca para bots no Telegram)  
- **CoinGecko API** (Dados de preços e ATH)  
- **CryptoPanic API** (Notícias sobre criptomoedas)  
- **Alternative.me API** (Índice de Medo e Ganância)  
- **Requests Cache** (Cache para otimizar chamadas à API)  

---

## 📂 **Estrutura do Projeto**  

```plaintext
chainalertbot/
│
├── main.py                # Arquivo principal do bot
├── config/
│   └── settings.py        # Configurações (token do bot, chaves de API)
├── .env                   # Variáveis de ambiente (API keys)
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

---

## 🔧 **Como Executar Localmente**  

### **1. Instale as dependências**  
```bash
pip install -r requirements.txt
```

### **2. Configure as variáveis de ambiente**  
Crie um arquivo `.env` com:  
```env
API_KEY_COINGECKO=sua_chave_aqui
API_KEY_CRYPTOPANIC=sua_chave_aqui
TELEGRAM_BOT_TOKEN=seu_token_aqui
```

### **3. Execute o bot**  
```bash
python main.py
```

---

## 📜 **Comandos Disponíveis**  

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Mensagem de boas-vindas | `/start` |
| `/preço` | Preço de uma criptomoeda | `/preço bitcoin` |
| `/top10` | Top 10 criptomoedas | `/top10` |
| `/ath` | Preço mais alto (ATH) | `/ath ethereum` |
| `/medo` | Índice de Medo e Ganância | `/medo` |
| `/noticias` | Últimas notícias | `/noticias` |
| `/alerta` | Configura um alerta | `/alerta solana 150 mais` |
| `/ajuda` | Lista de comandos | `/ajuda` |

---

## 📝 **Licença**  
MIT License - Livre para uso e modificação.  

---

Feito com ❤️ por **Lucas Betel** 🚀  
