# Ваш токен бота


from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем текст сообщения
    message_text = update.message.text
    # Выводим текст сообщения в терминал
    print(f"Received message: {message_text}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
