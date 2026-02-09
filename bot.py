import os
import telebot

# -------------------------------------
# Токен беремо з Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не заданий у Variables")

bot = telebot.TeleBot(BOT_TOKEN)

# -------------------------------------
# Читаємо список заборонених слів з файлу bad_words.txt
BAD_WORDS_FILE = "bad_words.txt"
try:
    with open(BAD_WORDS_FILE, "r", encoding="utf-8") as f:
        bad_words = [line.strip().lower() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Файл {BAD_WORDS_FILE} не знайдено! Список bad_words порожній.")
    bad_words = []

# -------------------------------------
# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привіт! Я на зв'язку 😊")

# -------------------------------------
# Модерація повідомлень
@bot.message_handler(func=lambda m: True)
def check_bad_words(message):
    text = message.text.lower()
    for word in bad_words:
        if word in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, f"Повідомлення видалено через заборонене слово: {word}")
            except Exception as e:
                print(f"Не вдалося видалити повідомлення: {e}")
            break

# -------------------------------------
# Запускаємо бота
bot.infinity_polling()
