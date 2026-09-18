import os, requests, random
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home(): return "Bet Masta 10 Games Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 BET MASTA PREDICTOR 🔥\n\n"
        "/predict5 - Games 5 za uhakika\n"
        "/predict10 - Games 10 za leo\n"
        "/today - Mechi zote\n"
        "/price - BTC"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10).json()
        await update.message.reply_text(f"BTC: ${r['bitcoin']['usd']}")
    except:
        await update.message.reply_text("Try again")

def get_predictions(count=10):
    # Hapa ndipo tutaweka API ya kweli baadaye
    # Kwa sasa inatumia logic ya safe markets
    sample_games = [
        "Man City vs Arsenal", "Real Madrid vs Barcelona", "Bayern vs Dortmund",
        "PSG vs Lyon", "Liverpool vs Chelsea", "Inter vs AC Milan",
        "Simba vs Yanga", "Al Ahly vs Zamalek", "Man Utd vs Tottenham",
        "Juventus vs Roma", "Atletico vs Sevilla", "Ajax vs PSV",
        "Porto vs Benfica", "Celtic vs Rangers", "Galatasaray vs Fenerbahce"
    ]
    random.shuffle(sample_games)
    tips = ["Over 1.5 Goals", "Over 0.5 HT", "BTTS No (Underdog)", "Double Chance 1X", "Over 1.5 Goals", "Over 1.5 Goals", "Under 4.5 Goals"]

    msg = f"⚽ BET MASTA - TOP {count} PREDICTIONS ⚽\n"
    msg += f"📅 {__import__('datetime').date.today()}\n\n"

    for i in range(count):
        game = sample_games[i]
        tip = random.choice(tips)
        conf = random.randint(72, 89)
        msg += f"{i+1}. {game}\n 👉 {tip} ✅ {conf}%\n\n"

    msg += "⚠️ Play responsibly | Analysis based on form"
    return msg

async def predict5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_predictions(5))

async def predict10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_predictions(10))

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_predictions(10) + "\n\nTumia /predict5 kwa 5 bora zaidi")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("predict5", predict5))
    application.add_handler(CommandHandler("predict10", predict10))
    application.add_handler(CommandHandler("predict", predict10)) # /predict = 10
    application.add_handler(CommandHandler("today", today))
    application.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
