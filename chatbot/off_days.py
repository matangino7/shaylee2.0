from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import params 
from datetime import datetime
def get_off_days(update: Update, context: CallbackContext):
    """
    get from user the days off for the next month, and pass it as a dict to backend
    """
    days_json = {}
    if context.user_data["authenticate"] == True:
        current_date = datetime.now()
        if current_date.day >= 15 and current_date.day < 26:
            while len(days_json) < 2:
                update.message.reply_text('dd-mm-yyyy: תכניס בבקשה את ימי ההסתייגויות שלך בפורמט')
                try:
                    date_input = datetime.strptime(update.message.text, current_date)
                    days_json[f'off_day{len(days_json) + 1}'] = date_input
                except:
                    update.message.reply_text("ישנה שגיאה בהודעה ששלחת, אנא שלח שוב")    
            while len(days_json) < 3:
                update.message.reply_text('dd-mm-yyyy: תכניס בבקשה את התאריך של יום חמישי של השבת הסתייגויות שלך בפורמט')
                try:
                    date_input = datetime.strptime(update.message.text, current_date)
                    days_json[f'off_day{len(days_json) + 1}'] = date_input
                except:
                    update.message.reply_text("ישנה שגיאה בהודעה ששלחת, אנא שלח שוב")        
            return days_json
        elif current_date.day < 15:
            update.message.reply_text("אפשר לשלוח הסתייגויות לחודש החדש, החל מה15 לחודש")        
        else:
            update.message.reply_text("אי אפשר לשלוח יותר הסתגוייות לחודש הבא")        
            