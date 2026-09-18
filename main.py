from flask import Flask
from threading import Thread
import os, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
flask_app=Flask(__name__)
@flask_app.route('/')
def home():return "Hunchos Bot Live!"
def run_web():flask_app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
Thread(target=run_web,daemon=True).start()
TOKEN=os.environ.get("BOT_TOKEN")
async def start(update,context):await update.message.reply_text("Bot Live /price")
async def price(update,context):
 b=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=10).json()
 await update.message.reply_text(f"BTC: {b['price']}")
if __name__=="__main__":
 app=Application.builder().token(TOKEN).build()
 app.add_handler(CommandHandler("start",start))
 app.add_handler(CommandHandler("price",price))
 print("Bot starting...");app.run_polling()
