import os
import telebot
import feedparser
import google.generativeai as genai

# Environment Variables များရယူခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini AI ကို Configure လုပ်ခြင်း
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# RSS Feeds URLs
TECH_FEED = "https://feeds.feedburner.com/TechCrunch/"
MYANMAR_FEED = "https://www.bbc.com/burmese/index.xml"

# Gemini သုံးပြီး ဘာသာပြန်ပေးမည့် function
def translate_and_tip(text):
    prompt = f"Translate this tech news to Myanmar language clearly. Also, provide a short useful AI tool tip at the end in Myanmar: {text}"
    response = model.generate_content(prompt)
    return response.text

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ။\n/tech - နည်းပညာသတင်းများ\n/myanmar - မြန်မာသတင်းများ")

@bot.message_handler(commands=['tech'])
def get_tech_news(message):
    bot.send_chat_action(message.chat.id, 'typing')
    feed = feedparser.parse(TECH_FEED)
    
    # နောက်ဆုံးရ သတင်း ၃ ပုဒ်ကို ယူမယ်
    news_update = ""
    for entry in feed.entries[:3]:
        news_update += f"🔹 {entry.title}\n"
    
    # Gemini နဲ့ ဘာသာပြန်မယ် + AI Tip ယူမယ်
    result = translate_and_tip(news_update)
    bot.reply_to(message, f"📢 **နည်းပညာသတင်းနှင့် AI လက်ဆောင်**\n\n{result}")

@bot.message_handler(commands=['myanmar'])
def get_myanmar_news(message):
    bot.send_chat_action(message.chat.id, 'typing')
    feed = feedparser.parse(MYANMAR_FEED)
    
    msg = "🇲🇲 **မြန်မာသတင်းများ**\n\n"
    for entry in feed.entries[:5]:
        msg += f"📌 {entry.title}\n🔗 {entry.link}\n\n"
    
    bot.reply_to(message, msg)

# Bot ကို စတင် run ခြင်း
print("Bot is running...")
bot.infinity_polling()

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

        return f"TRANSLATE ERROR: empty response"

    except Exception as e:
        return f"TRANSLATE ERROR: {str(e)}"


def get_feed_news(feed_url, limit=3):
    feed = feedparser.parse(feed_url)
    news = ""

    for entry in feed.entries[:limit]:
        translated_title = translate_to_myanmar(entry.title)
        news += f"📰 {translated_title}\n{entry.link}\n\n"

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
