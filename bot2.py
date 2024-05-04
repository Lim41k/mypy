
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
TOKEN = os.getenv('TOKEN')
chat_id = os.getenv('chat_id')

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    keyboard = [[InlineKeyboardButton("Current BTC Price", callback_data='btc')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose:', reply_markup=reply_markup)
    

async def btc_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    btc_data = response.json()
    print(btc_data['bitcoin']['usd'])
    btc_price_usd = btc_data['bitcoin']['usd']
    await update.callback_query.answer(text=f'Current BTC Price: {btc_price_usd} USD')


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CallbackQueryHandler(btc_price, pattern='btc'))

print("bot run ...")

app.run_polling()

print("bot stop!")
