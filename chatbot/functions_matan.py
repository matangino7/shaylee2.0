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


def send_dates(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Great! Please provide three dates in the format dd-mm-yyyy.')
    context.user_data['dates'] = []

def collect_dates(update: Update, context: CallbackContext) -> None:
    if 'dates' not in context.user_data:
        context.user_data['dates'] = []

    if len(context.user_data['dates']) < 3:
        try:
            date_str = update.message.text
            date_object = datetime.strptime(date_str, "%d-%m-%Y")
            context.user_data['dates'].append(date_object)
            update.message.reply_text(f'Thank you! Date {len(context.user_data["dates"])} received.')
        except ValueError:
            update.message.reply_text('Invalid date format. Please use dd-mm-yyyy.')

    if len(context.user_data['dates']) == 3:

        user_id = update.message.from_user.id
        try:
            response = requests.post(f'{params.senddates_endpoint}{context.user_data["id"]}', json={'off_day1': context.user_data['dates'][0], 'off_day2': context.user_data['dates'][1], 'off_weekend': context.user_data['dates'][2]})
            if response.status_code == 200:
                update.message.reply_text('Dates submitted successfully!')
            else:
                update.message.reply_text('Failed to submit dates. Please try again later.')
        except Exception as e:
            update.message.reply_text(f'An error occurred: {str(e)}') 
            

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