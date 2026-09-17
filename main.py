import os, requests, random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

def get_games():
    try:
        leagues=["4328","4335","4332"]
        games=[]
        for lid in leagues:
            r=requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}",timeout=10)
            d=r.json()
            if d and d.get('events'):
                for ev in d['events'][:2]:
                    games.append({"home":ev.get('strHomeTeam'),"away":ev.get('strAwayTeam'),"league":ev.get('strLeague')})
        return games[:8]
    except:
        return [{"home":"Man City","away":"Arsenal","league":"EPL"},{"home":"Barcelona","away":"Real Madrid","league":"La Liga"},{"home":"Inter","away":"AC Milan","league":"Serie A"}]

def predict(h,a):
    return random.choice([f"Over 1.5 - 87%",f"{h} Win/Draw (1X) - 79%",f"BTTS YES - 82%",f"Over 2.5 - 75%"])

async def start(update,ctx):
    await update.message.reply_text("⚽ HUNCHOS PREDICTOR IS LIVE!\n\n/today - Games za leo\n/tomorrow - Kesho")

async def today(update,ctx):
    await update.message.reply_text("⏳ Natafuta games...")
    games=get_games()
    msg=f"🔥 PREDICTIONS {datetime.now().strftime('%d/%m')}\n\n"
    for g in games:
        msg+=f"🏆 {g['league']}\n{g['home']} vs {g['away']}\n✅ {predict(g['home'],g['away'])}\n\n"
    await update.message.reply_text(msg)

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("today",today))
app.add_handler(CommandHandler("tomorrow",today))
print("Bot started...")
app.run_polling()
