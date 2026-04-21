import os
import feedparser
import google.generativeai as genai

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Telegram Token (direct) ===
TOKEN = "8579322843:AAEvVt7yUHeWquXPNisfHJJuVJ5aJwuX5Tw"

# === Gemini API key (from environment variable) ===
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# === RSS Feeds ===
TECH_FEED = "https://feeds.feedburner.com/TechCrunch"
MYANMAR_FEED = "https://rss.app/feeds/AmeVJCd8XByk6J6R.xml"

# === Gemini setup ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# === Translate function ===
def translate_to_myanmar(text):
    try:
        prompt = f"Translate this into natural Burmese language only:\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return text


# === Get news function ===
def get_feed_news(feed_url, limit=3):
    feed = feedparser.parse(feed_url)
    news = ""

    for entry in feed.entries[:limit]:
        title = translate_to_myanmar(entry.title)
        news += f"📰 {title}\n{entry.link}\n\n"

    return news if news else "No news found."


# === Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "မင်္ဂလာပါ 👋\n\n"
    msg += "/tech - Tech news (မြန်မာဘာသာ)\n"
    msg += "/myanmar - Myanmar news (မြန်မာဘာသာ)"
    await update.message.reply_text(msg)


async def tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🤖 Tech News (မြန်မာ)\n\n"
    msg += get_feed_news(TECH_FEED)
    await update.message.reply_text(msg)


async def myanmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🇲🇲 Myanmar News (မြန်မာ)\n\n"
    msg += get_feed_news(MYANMAR_FEED)
    await update.message.reply_text(msg)


# === Run bot ===
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tech", tech))
app.add_handler(CommandHandler("myanmar", myanmar))

PORT = int(os.environ.get("PORT", 10000))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url="https://telegram-news-bot-1-b899.onrender.com"
)
