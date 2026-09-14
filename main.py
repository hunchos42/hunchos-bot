import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token inatoka Render, sio hapa - secure!
TOKEN = os.environ.get("TOKEN")
MY_PROFIT = 1.5

def get_binance_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTKES", timeout=10).json()
        return float(r['price'])
    except:
        return 129.5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Hunchos P2P LIVE!\n\n/price - bei ya leo\n/buy - kununua")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    binance = get_binance_price()
    yangu = binance + MY_PROFIT
    await update.message.reply_text(f"💰 Bei leo:\nBinance: {binance:.2f} KES\nYangu: {yangu:.2f} KES\nFaida: {MY_PROFIT}")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nunua:\n1. Tuma KES M-Pesa: 07XX...\n2. Tuma USDT address\n3. Nikutumie haraka!")

# Muhimu kwa Render
print("Bot ina-start...")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("buy", buy))

app.run_polling()
