from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import sqlite3

from fake_useragent import UserAgent

import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 
TOKEN = os.getenv('TOKEN')
chat_id = os.getenv('chat_id')
bot = TOKEN

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    cursor.execute('''SELECT DISTINCT name, link 
                      FROM serials 
                      WHERE name = ? AND num = 1 AND season = 1;''', (message_text,))
    rows = cursor.fetchall()
    if rows:
        row = rows[0]
        name, link = row[0], row[1]
        await context.bot.send_message(chat_id, f"{name}: {link}")  # Используйте `await` для дожидания завершения отправки сообщения
    else:
        await context.bot.send_message(chat_id, "Сериал не найден")

    # Закрываем соединение с базой данных
  


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
connection.close()