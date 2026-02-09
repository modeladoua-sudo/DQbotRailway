from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread

# ====== 1. Токен бота ======
TOKEN_FILE = "DQLG.txt"
with open(TOKEN_FILE, "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()

# ====== 2. Список заборонених слів ======
BAD_WORDS_FILE = "bad_words.txt"
with open(BAD_WORDS_FILE, "r", encoding="utf-8") as f:
    BAD_WORDS = [line.strip() for line in f if line.strip()]

# ====== 3. Команда /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я на звʼязку 🤖")

# ====== 4. Перевірка повідомлень ======
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(update.message.text.lower().split())
    for word in BAD_WORDS:
        normalized_word = ' '.join(word.lower().split())
        if normalized_word in text:
            await update.message.delete()
            await update.message.reply_text(
                f"{update.effective_user.first_name}, повідомлення видалено 🚫"
            )
            break

# ====== 5. Створення бота ======
app_bot = ApplicationBuilder().token(TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

# ====== 6. Вбудований веб-сервер ======
app_flask = Flask("")

@app_flask.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=8000)

Thread(target=run_flask).start()

# ====== 7. Запуск бота ======
app_bot.run_polling()
