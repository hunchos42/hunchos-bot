import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")
MY_PROFIT = 1.5
WHATSAPP_NUMBER = "254757880062"

def get_binance_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTKES", timeout=10).json()
        return float(r['price'])
    except:
        return 131.5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Hunchos P2P LIVE!\n\n/price - bei ya leo\n/buy - nunua USDT")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    binance = get_binance_price()
    yangu = binance + MY_PROFIT
    await update.message.reply_text(f"💰 Bei leo:\nBinance: {binance:.2f} KES\nYangu: {yangu:.2f} KES")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    binance = get_binance_price()
    yangu = binance + MY_PROFIT
    text = f"Sasa bro, nahitaji USDT 100 kwa bei {yangu:.2f}"
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={requests.utils.quote(text)}"
    keyboard = [[InlineKeyboardButton("💬 Chat WhatsApp Sasa", url=wa_link)]]
    await update.message.reply_text(
        f"Tayari kununua kwa {yangu:.2f} KES per USDT?\nBonyeza chini unicheki WhatsApp:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

print("Bot ina-start...")
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("buy", buy))
app.run_polling()
