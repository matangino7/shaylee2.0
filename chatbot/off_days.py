from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import params 
import datetime
def get_off_days(update: Update, context: CallbackContext):
    user_id = context.user_data["id"]
    if context.user_data["authenticate"] == True:
        # if datetime.
        update.message.reply_text('dd/mm/yyyy: תכניס בבקשה את ימי ההסתייגויות שלך בפורמט')


