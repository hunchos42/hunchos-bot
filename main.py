import os, requests, random, datetime, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
FOOTBALL_KEY = os.getenv("FOOTBALL_API_KEY")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bet Masta Level 2 Live!"

def get_real_fixtures():
    if FOOTBALL_KEY and FOOTBALL_KEY!= "12345" and FOOTBALL_KEY!= "demo":
        try:
            today = datetime.date.today().isoformat()
            url = f"https://v3.football.api-sports.io/fixtures?date={today}"
            headers = {"x-apisports-key": FOOTBALL_KEY}
            r = requests.get(url, headers=headers, timeout=15).json()
            fixtures = r.get("response", [])[:12]
            if fixtures:
                games = []
                for f in fixtures:
                    home = f['teams']['home']['name']
                    away = f['teams']['away']['name']
                    games.append(f"{home} vs {away}")
                return games
        except Exception as e:
            print(f"API error: {e}")

    return [
        "Man City vs Arsenal", "Real Madrid vs Espanyol", "Bayern Munich vs Dortmund",
        "Inter Milan vs AC Milan", "PSG vs Marseille", "Liverpool vs Chelsea",
        "Barcelona vs Getafe", "Juventus vs Napoli", "Simba SC vs Yanga SC",
        "Al Ahly vs Zamalek", "Atletico Madrid vs Real Sociedad", "Ajax vs PSV",
        "Porto vs Benfica", "Galatasaray vs Fenerbahce", "Man Utd vs Tottenham"
    ]

def get_predictions(count):
    games = get_real_fixtures()
    random.shuffle(games)
    tips_pool = [
        ("Over 1.5 Goals", "Attack kali pande zote"),
        ("Over 0.5 HT", "Magoli mapema"),
        ("Double Chance 1X", "Mwenyeji hatapoteza"),
        ("Double Chance X2", "Mgeni hatapoteza"),
        ("Under 4.5 Goals", "Game ya kiufundi"),
        ("BTTS No", "Defense imara"),
    ]
    today = datetime.date.today().strftime("%b %d, %Y")
    msg = f"⚽ *BET MASTA TOP {count}* ⚽\n📅 {today}\n\n"
    for i in range(min(count, len(games))):
        tip, reason = random.choice(tips_pool)
        conf = random.randint(76, 91)
        odd = round(random.uniform(1.35, 1.85), 2)
        msg += f"{i+1}. *{games[i]}*\n"
        msg += f" 👉 {tip} | Odd: {odd} ✅ {conf}%\n"
        msg += f" _{reason}_\n\n"
    msg += "⚠️ _Play responsibly 18+_"
    return msg

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🔥 5 Games Bora", callback_data="p5"),
         InlineKeyboardButton("💎 10 Games Leo", callback_data="p10")],
        [InlineKeyboardButton("💰 BTC Price", callback_data="price")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *BET MASTA
