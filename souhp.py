import os
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import random
from threading import Thread
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Create a new event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Bot Configuration
TOKEN = '7757010456:AAECe5GcIFXjLrYhZDMRVXZv0jebPxhORRI'
ADMIN_USER_ID = 6353114118
MONGO_URI = 'mongodb+srv://sharp:sharp@sharpx.x82gx.mongodb.net/?retryWrites=true&w=majority&appName=SharpX'
USERNAME = "@N9MANxHERO"

# Attack Settings
attack_in_progress = False
attack_settings = {
    "byte_size": 1000,
    "thread_size": 10,
    "attack_time": 60
}

# Logging Configuration
logging.basicConfig(format='%(asctime)s - ⚔️ %(message)s', level=logging.INFO)

# MongoDB Setup
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['sharp']
users_collection = db.users
codes_collection = db.codes

# Bot Initialization
bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

async def start_asyncio_thread():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

# Code Generation Command
@bot.message_handler(commands=['gen'])
def generate_code(message):
    # (Content remains unchanged from your code)
    pass

# Code Redemption Command
@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    # (Content remains unchanged from your code)
    pass

# Set Byte Size Command
@bot.message_handler(commands=['byte'])
def set_byte_size(message):
    # (Content remains unchanged from your code)
    pass

# Set Thread Size Command
@bot.message_handler(commands=['thread'])
def set_thread_size(message):
    # (Content remains unchanged from your code)
    pass

# Set Attack Time Command
@bot.message_handler(commands=['set_time'])
def set_attack_time(message):
    # (Content remains unchanged from your code)
    pass

# Proxy Update Command
@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    # (Content remains unchanged from your code)
    pass

def update_proxy():
    # (Content remains unchanged from your code)
    pass

# Attack Command
@bot.message_handler(commands=['attack'])
def attack_command(message):
    global attack_in_progress
    chat_id = message.chat.id

    if attack_in_progress:
        bot.send_message(chat_id, f"⚠️ *An attack is already in progress. Please wait until it completes, {USERNAME}.*", parse_mode='Markdown')
        return

    try:
        args = message.text.split()
        if len(args) != 4:
            bot.send_message(chat_id, "⚠️ *Usage: /attack <IP> <Port> <Duration>*", parse_mode='Markdown')
            return

        target_ip, target_port, duration = args[1], int(args[2]), int(args[3])

        if target_port in blocked_ports:
            bot.send_message(chat_id, f"🚫 *Port {target_port} is restricted. Choose a different port.*", parse_mode='Markdown')
            return

        attack_in_progress = True
        bot.send_message(chat_id, f"🔥 *Attack started on {target_ip}:{target_port} for {duration} seconds!*", parse_mode='Markdown')

        # Simulate attack process
        time.sleep(duration)

        attack_in_progress = False
        bot.send_message(chat_id, f"✅ *Attack on {target_ip}:{target_port} completed!*", parse_mode='Markdown')

    except Exception as e:
        logging.error(f"Error in /attack: {e}")
        bot.send_message(chat_id, f"⚠️ *Failed to start the attack. Error: {e}*", parse_mode='Markdown')

# Start Command
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    options = ["💀 Initiate Attack", "📜 Mission Brief"]
    buttons = [KeyboardButton(option) for option in options]
    markup.add(*buttons)

    bot.send_message(
        chat_id,
        f"👋 *Welcome to the bot! Use the menu or type commands directly.*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# Main Function
if __name__ == "__main__":
    # Run asyncio thread
    asyncio_thread = Thread(target=lambda: loop.run_until_complete(start_asyncio_thread()), daemon=True)
    asyncio_thread.start()
    logging.info("\U0001F680 Bot is operational and mission-ready.")

    try:
        # Use infinity_polling to handle updates without conflicts
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logging.error(f"Polling error: {e}")
