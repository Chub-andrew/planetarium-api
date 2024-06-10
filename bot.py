import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

from telegram_bot.commands_handlers import start

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if TELEGRAM_TOKEN is None:
    raise ValueError("No TELEGRAM_TOKEN found in environment variables")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
