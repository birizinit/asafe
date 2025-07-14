import datetime
import asyncio
import schedule
import time
import random
import threading
import os
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from zoneinfo import ZoneInfo

# === CONFIGURAÇÃO ===
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

# === LISTAS DE OPÇÕES ===
ATIVOS = [
    "BNB/USDT", "XRP/USD", "BTC/USD",
    "ETH/USDT", "DOGE/USD", "SOL/USD",
]

DIRECOES = ["🟢 COMPRA", "🔴 VENDA"]

# === STICKERS ===
STICKERS_LOSS = [
    "CAACAgEAAxkBAAEO1S9oZLqK51G0NHn2Fp92eApnV197kgAC0hgAAjwoKUfF_ztlB4K_WTYE"
]
STICKER_WIN = "CAACAgEAAxkBAAEO1TFoZLqV8E_HeQPaiDJdocq-m4DoBAACzwUAAq0LKUdb9LY94CbSXjYE"

# === LOOP DO ASYNCIO EM BACKGROUND ===
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
def start_loop():
    loop.run_forever()
threading.Thread(target=start_loop, daemon=True).start()

# === FUNÇÃO ASSÍNCRONA PARA ENVIAR MENSAGEM COM BOTÃO ===
async def enviar_mensagem(texto):
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Abrir Corretora", url="https://traderoom.asafebroker.com/?code=9649")]
    ])
    await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown", reply_markup=teclado)

# === FUNÇÃO ASSÍNCRONA PARA ENVIAR RESULTADO COM STICKER ===
async def enviar_resultado_async(ativo, direcao):
    chance_win = random.randint(60, 89)
    is_win = random.randint(1, 100) <= chance_win

    if is_win:
        await bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_WIN)
    else:
        for sticker_loss in STICKERS_LOSS:
            await bot.send_sticker(chat_id=CHAT_ID, sticker=sticker_loss)

# === FUNÇÃO ASSÍNCRONA PARA AGENDAR RESULTADO APÓS 3 MINUTOS ===
async def agendar_envio_resultado(ativo, direcao):
    await asyncio.sleep(180)
    await enviar_resultado_async(ativo, direcao)

# === FUNÇÃO ASSÍNCRONA PARA ENVIAR SINAL ===
async def enviar_sinal():
    agora = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))

    entrada_time = agora + datetime.timedelta(minutes=4)
    gale1_time = entrada_time + datetime.timedelta(minutes=1)
    gale2_time = entrada_time + datetime.timedelta(minutes=2)

    entrada = entrada_time.strftime("%H:%M")
    gale1 = gale1_time.strftime("%H:%M")
    gale2 = gale2_time.strftime("%H:%M")

    ativo = random.choice(ATIVOS)
    direcao = random.choice(DIRECOES)

    mensagem = f"""✅ *ENTRADA CONFIRMADA* ✅

🌎 *Ativo:* {ativo}
⏳ *Expiração:* M1
📊 *Direção:* {direcao}
⏰ *Entrada:* {entrada}

👉 *Fazer até 2 martingale em caso de loss!*
1º GALE: *TERMINA EM:* {gale1}h
2º GALE: *TERMINA EM:* {gale2}h
"""
    await enviar_mensagem(mensagem)
    asyncio.create_task(agendar_envio_resultado(ativo, direcao))

# === FUNÇÃO DE AGENDAMENTO ===
def agendar_envio():
    asyncio.run_coroutine_threadsafe(enviar_sinal(), loop)

# === AGENDAMENTO A CADA 15 MINUTOS ===
schedule.every(15).minutes.do(agendar_envio)

# === ENVIA UM SINAL IMEDIATO AO INICIAR ===
agendar_envio()

# === LOOP PRINCIPAL DO SCRIPT ===
while True:
    schedule.run_pending()
    time.sleep(1)
