import os, requests, random, datetime, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bet Masta 10 Games Live!"

def get_predictions(count):
    games = [
        "Man City vs Arsenal", "Real Madrid vs Barcelona", "Bayern vs Dortmund",
        "PSG vs Lyon", "Liverpool vs Chelsea", "Inter vs AC Milan",
        "Simba vs Yanga", "Al Ahly vs Zamalek", "Man Utd vs Tottenham",
        "Juventus vs Roma", "Atletico vs Sevilla", "Ajax vs PSV",
        "Porto vs Benfica", "Celtic vs Rangers", "Galatasaray vs Fenerbahce"
    ]
    random.shuffle(games)
    tips = ["Over 1.5 Goals", "Over 0.5 HT", "Double Chance 1X", "Under 4.5 Goals"]
    today = datetime.date.today().strftime("%b %d")
    msg = f"⚽ BET MASTA TOP {count} ⚽\n📅 {today}\n\n"
    for i in range(count):
        conf = random.randint(75, 88)
        msg += f"{i+1}. {games[i]}\n 👉 {random.choice(tips)} ✅ {conf}%\n\n"
    return msg + "⚠️ Play responsibly"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Karibu Bet Masta!\n/predict5 - 5 games\n/predict10 - 10 games")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10).json()
        await update.message.reply_text(f"BTC: ${r['bitcoin']['usd']}")
    except:
        await update.message.reply_text("Try again")

async def p5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_predictions(5))

async def p10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_predictions(10))

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask in background
    threading.Thread(target=run_flask, daemon=True).start()
    # Bot in MAIN thread - hii ndio fix
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("predict5", p5))
    application.add_handler(CommandHandler("predict10", p10))
    application.add_handler(CommandHandler("predict", p10))
    application.add_handler(CommandHandler("today", p10))
    print("BOT POLLING STARTED - 10 games ready")
    application.run_polling(drop_pending_updates=True)
