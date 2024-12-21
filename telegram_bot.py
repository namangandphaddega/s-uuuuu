import logging
import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define admin ID(s)
ADMIN_IDS = [6353114118]  # Replace with your Telegram user ID

# User data with expiration dates
user_access = {}

# Helper function to check if a user is an admin
def is_admin(user_id):
    return user_id in ADMIN_IDS

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_access and user_access[user_id] > datetime.now():
        await update.message.reply_text("Welcome back! You have access.")
    else:
        await update.message.reply_text("Hello! You currently don't have access. Contact an admin.")

# Command: /allow <user_id> <plan_id> <days>
async def allow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) != 3:
        await update.message.reply_text("Usage: /allow <user_id> <plan_id> <days>")
        return

    try:
        user_id = int(context.args[0])
        plan_id = context.args[1]
        days = int(context.args[2])
        expiration_date = datetime.now() + timedelta(days=days)
        user_access[user_id] = expiration_date

        await update.message.reply_text(
            f"User {user_id} has been granted access under Plan {plan_id} for {days} days, until {expiration_date}."
        )
    except ValueError:
        await update.message.reply_text("Invalid input. Please ensure user_id and days are numbers.")

# Command: /check <user_id>
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /check <user_id>")
        return

    try:
        user_id = int(context.args[0])
        if user_id in user_access:
            expiration_date = user_access[user_id]
            if expiration_date > datetime.now():
                await update.message.reply_text(f"User {user_id} has access until {expiration_date}.")
            else:
                await update.message.reply_text(f"User {user_id}'s access has expired.")
        else:
            await update.message.reply_text(f"User {user_id} does not have access.")
    except ValueError:
        await update.message.reply_text("Invalid user_id. Please ensure it is a number.")

# Command: /attack <ip> <port> <time>
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_access or user_access[user_id] <= datetime.now():
        await update.message.reply_text("You don't have access to use this command. Contact an admin.")
        return

    if len(context.args) != 3:
        await update.message.reply_text("Usage: /attack <ip> <port> <time>")
        return

    ip = context.args[0]
    port = context.args[1]
    duration = context.args[2]

    await update.message.reply_text(f"Attack initiated on IP: {ip}, Port: {port}, Duration: {duration} seconds.")

# Main function
def main():
    token = "7577700170:AAGi3lcPU5Fgk5g1KAnVyr9f_xxd7QdGBOw"  # Replace with your bot token
    application = Application.builder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("allow", allow))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("attack", attack))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
