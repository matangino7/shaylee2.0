from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import functions_matan
from flask import Flask, request
from threading import Thread
from werkzeug.serving import run_simple
import params 


app = Flask(__name__)
updater = Updater(token=params.api_token)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('שלום, אני בוט שמסייע בארגון השמירות בצה״ל למידע על פקודות נא להקיש /help')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


@app.route("/broadcast", methods=["POST"])
def trigger_broadcast():
    """Endpoint to trigger a broadcast."""
    try:
        message = request.json.get("message", "Default broadcast message")
        success = functions_matan.broadcast_message_to_users(updater.dispatcher, message)
        if success:
            return "Broadcast triggered successfully!"
        else:
            return "Error triggering broadcast. Please try again.", 500
    except Exception as e:
        return f"Error triggering broadcast: {e}", 500
    

def run_flask():
    run_simple("127.0.0.1", 5020, app, use_reloader=False, threaded=True)


def main() -> None:
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", functions_matan.login))
    dispatcher.add_handler(CommandHandler("help", functions_matan.help))
    dispatcher.add_handler(CommandHandler("off_days", functions_matan.get_off_days))
    updater.start_polling(timeout=10)
    updater.idle()


if __name__ == '__main__':
    main()