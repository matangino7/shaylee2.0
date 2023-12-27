from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import params 


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your Telegram bot.')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    updater = Updater(token=params.api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling(timeout=10)
    updater.idle()


if __name__ == '__main__':
    main()