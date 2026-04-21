import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8579322843:AAH6KXxO0kEcykE6U5-c96-fA0IvODEQwqk"

TECH_FEED = "https://feeds.feedburner.com/TechCrunch/"
MYANMAR_FEED = "https://rss.app/feeds/AmeVJCd8XByk6J6R.xml"

def get_feed_news(feed_url, limit=3):
    feed = feedparser.parse(feed_url)
    news = ""
    for entry in feed.entries[:limit]:
        news += f"📰 {entry.title}\n{entry.link}\n\n"
    return news if news else "No news found."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "မင်္ဂလာပါ 👋\n\n"
    msg += "/tech - Tech AI tool tip news\n"
    msg += "/myanmar - Myanmar news\n"
    await update.message.reply_text(msg)

async def tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🤖 Tech / AI Tool Tip News\n\n"
    msg += get_feed_news(TECH_FEED)
    await update.message.reply_text(msg)

async def myanmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🇲🇲 Myanmar News\n\n"
    msg += get_feed_news(MYANMAR_FEED)
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tech", tech))
app.add_handler(CommandHandler("myanmar", myanmar))

app.run_polling()
