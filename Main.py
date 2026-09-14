from flask import Flask
import threading, asyncio, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

MPESA_NUMBER = "0181052018"
BOT_TOKEN = "8915658393:AAE5El4_evv7aPk4RciLUE-2TX75KZtpMVw"

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Hunchos Bot LIVE 24/7!"

async def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTKES", timeout=5).json()
        return float(r['price'])
    except: return 131.5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hunchos LIVE 24/7!\n/price - bei\n/buy - nunua")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = await get_price()
    await update.message.reply_text(f"Binance: {p} KES\nYangu: {p+1} KES")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Tuma KES kwa M-Pesa: {MPESA_NUMBER}\nKisha tuma USDT address")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("buy", buy))
    await app.initialize(); await app.start()
    await app.updater.start_polling()
    print("Bot LIVE...")
    await asyncio.Event().wait()

def start_bot(): asyncio.run(run_bot())

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app_flask.run(host="0.0.0.0", port=10000)
