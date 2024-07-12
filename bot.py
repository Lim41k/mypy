

# Ваш токен бота
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
print("Bot start")
load_dotenv() 
TOKEN = os.getenv('TOKEN')
chat_id = os.getenv('chat_id')

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    print(message_text)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, чего изволите?')


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))


print("Bot run")
app.run_polling()
