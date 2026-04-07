import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔐 ENV VARIABLES
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🧠 GEMINI FUNCTION
def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload, timeout=30)

        # 🔍 DEBUG LOGS
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            return "❌ حصل مشكلة في الاتصال بالذكاء الاصطناعي"

        data = response.json()

        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "❌ مفيش رد من Gemini"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# 👋 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بيك! ابعتلي أي رسالة وهرد عليك بالذكاء الاصطناعي 🤖")


# 💬 MESSAGE HANDLER
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # ⏳ رسالة انتظار
    msg = await update.message.reply_text("🤔 Thinking...")

    reply = ask_gemini(user_text)

    # ✏️ تعديل نفس الرسالة بدل ما يبعت 2
    await msg.edit_text(reply)


# 🚀 MAIN
def main():
    if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
        print("❌ لازم تحط التوكنز في Environment Variables")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🚀 Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
