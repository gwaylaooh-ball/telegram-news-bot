import os
import telebot
import feedparser
import google.generativeai as genai

# Environment Variables ယူခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini ကို Configure လုပ်ခြင်း (Model နာမည်ကို သေချာအောင် models/ ထည့်ထားပါတယ်)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# RSS Feeds URLs
TECH_FEED = "https://feeds.feedburner.com/TechCrunch/"
MYANMAR_FEED = "https://www.bbc.com/burmese/index.xml"

def translate_and_tip(text):
    try:
        prompt = f"Translate this tech news to Myanmar language clearly. Also, provide a short useful AI tool tip at the end in Myanmar: {text}"
        response = model.generate_content(prompt)
        # ဒီနေရာမှာ Indent (ကွက်လပ်) မှန်ဖို့ အရမ်းအရေးကြီးပါတယ်
        if response and hasattr(response, 'text'):
            return response.text
        return "⚠️ ဘာသာပြန်ဆိုချက် မရရှိနိုင်ပါ။"
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "⚠️ Gemini API Error တက်နေပါသည်။"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ။\n/tech - နည်းပညာသတင်းများ\n/myanmar - မြန်မာသတင်းများ")

@bot.message_handler(commands=['tech'])
def get_tech_news(message):
    bot.send_chat_action(message.chat.id, 'typing')
    feed = feedparser.parse(TECH_FEED)
    news_update = ""
    for entry in feed.entries[:3]:
        news_update += f"🔹 {entry.title}\n"
    
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

# Bot စတင်ခြင်း
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
