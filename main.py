from flask import Flask
from threading import Thread
import os, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Flask keep-alive for Render ---
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Hunchos Bot Live!"
def run_web():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
Thread(target=run_web, daemon=True).start()

# --- Telegram Bot ---
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hunchos Bot iko Live 🔥 /price /news /signals")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        await update.message.reply_text(f"BTC: ${btc['price']}")
    except:
        await update.message.reply_text("Error kupata price")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    print("Bot starting...")
    app.run_polling()
