import os
import telebot
import feedparser
import google.generativeai as genai
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_dummy_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not BOT_TOKEN or not GEMINI_API_KEY:
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

TECH_FEED = "https://feeds.feedburner.com/TechCrunch/"
MYANMAR_FEED = "https://www.bbc.com/burmese/index.xml"

def translate_and_tip(text):
    try:
        prompt = f"Translate this tech news to Myanmar language clearly. Also, provide a short useful AI tool tip at the end in Myanmar: {text}"
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text'):
            return response.text
        return "⚠️ ဘာသာပြန်ဆိုချက် မရရှိနိုင်ပါ။"
    except Exception:
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

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    bot.infinity_polling()
