from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import requests
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
