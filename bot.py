from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")

# Завантаження заборонених слів
def load_bad_words():
    try:
        with open("bad_words.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print("bad_words.txt not found")
        return []

BAD_WORDS = load_bad_words()

async def moderate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    for word in BAD_WORDS:
        if word in text:
            try:
                await update.message.delete()
                print(f"Deleted message: {text}")
            except Exception as e:
                print(f"Delete error: {e}")
            break

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        moderate
    )
)

app.run_polling()
