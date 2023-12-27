from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import functions_matan
import params 


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('שלום, אני בוט שמסייע בארגון השמירות בצה״ל למידע על פקודות נא להקיש /help')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    updater = Updater(token=params.api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", functions_matan.login))
    dispatcher.add_handler(CommandHandler("help", functions_matan.help))
    updater.start_polling(timeout=10)
    updater.idle()


if __name__ == '__main__':
    main()