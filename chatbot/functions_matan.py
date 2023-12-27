from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import requests
from datetime import datetime
import params


def login(update: Update, context: CallbackContext) -> None:
    """
    this is the login function
    """
    try:
        if len(context.args) != 2:
            update.message.reply_text("Usage: /login <id> <password>")
            return

        id, password = context.args
        my_request = requests.api.post(
            params.login_endpoint, json={"id": id, "password": password}
        )

        my_request.raise_for_status()

        response_data = my_request.json()
        if response_data.get('success', False):
            context.user_data["authenticated"] = True
            context.user_data["id"] = id
            update.message.reply_text("Login successful! You are now authenticated.")
        else:
            context.user_data["authenticated"] = False
            update.message.reply_text("Invalid credentials. Login failed.")

    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"ישנה תקלה בהיתחברות, נסה שנית מאוחר יותר")

    except Exception as e:
        update.message.reply_text(f"An unexpected error occurred")


def help(update: Update, context: CallbackContext):
    """
    this is the help function
    """
    update.message.reply_text("/login בפקודה זו תוכל להתחבר על ממנת לשלוח הסתייגויות במערכת, יש לפנות לאחראי ביחידה על מנת להנפיק פרטים")
    update.message.reply_text("/off_days בפקודה זו תוכל להגיש הסתיגויות כאשר זה פתוח במערכת")


def get_off_days(update: Update, context: CallbackContext):
    """
    get from user the days off for the next month, and pass it as a dict to backend
    """
    days_json = {}
    current_date = datetime.now()
    date_format = '%Y-%m-%d'
    if current_date.day >= 15 and current_date.day < 28:
        while len(days_json) < 2:
            update.message.reply_text('dd-mm-yyyy: תכניס בבקשה את ימי ההסתייגויות שלך בפורמט')
            message = context.args[0] if context.args else None
            date_input = datetime.strptime(message, date_format)
            days_json[f'off_day{len(days_json) + 1}'] = date_input
        while len(days_json) < 3:
            update.message.reply_text('dd-mm-yyyy: תכניס בבקשה את התאריך של יום חמישי של השבת הסתייגויות שלך בפורמט')
            message = context.args[0] if context.args else None
            date_input = datetime.strptime(message, date_format)
            days_json[f'off_day{len(days_json) + 1}'] = date_input
            update.message.reply_text("ישנה שגיאה בהודעה ששלחת, אנא שלח שוב")        
        return days_json
    elif current_date.day < 15:
        update.message.reply_text("אפשר לשלוח הסתייגויות לחודש החדש, החל מה15 לחודש")        
    else:
        update.message.reply_text("אי אפשר לשלוח יותר הסתגוייות לחודש הבא")        
            

def broadcast_message_to_users(context: CallbackContext, message):
    """
    Function to broadcast a message to all authenticated users.
    """
    authenticated_users = [
        user_id
        for user_id, data in context.user_data.items()
        if data.get("authenticated", False)
    ]

    try:
        for user_id in authenticated_users:
            context.bot.send_message(chat_id=user_id, text=message)
        return True
    except Exception as e:
        print(f"Error sending broadcast message: {e}")
        return False