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
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Bot Configuration: Set with Authority
TOKEN = '7757010456:AAECe5GcIFXjLrYhZDMRVXZv0jebPxhORRI'
ADMIN_USER_ID = 6353114118
MONGO_URI = 'mongodb+srv://sharp:sharp@sharpx.x82gx.mongodb.net/?retryWrites=true&w=majority&appName=SharpX'
USERNAME = "@N9MANxHERO"  # Immutable username for maximum security

# Attack Status Variable to Control Single Execution
attack_in_progress = False
attack_settings = {
    "byte_size": 1000,  # Default byte size
    "thread_size": 10,  # Default thread size
    "attack_time": 60   # Default attack time in seconds
}

# Logging for Precision Monitoring
logging.basicConfig(format='%(asctime)s - ⚔️ %(message)s', level=logging.INFO)

# MongoDB Connection - Operative Data Storage
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['sharp']
users_collection = db.users
codes_collection = db.codes  # Collection to store generated codes

# Bot Initialization
bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

# Replace old asyncio loop handling
async def main():
    logging.info("\U0001F680 Bot is operational and mission-ready.")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Polling error: {e}")

# Code Generation Command
@bot.message_handler(commands=['gen'])
def generate_code(message):
    try:
        if message.from_user.id != ADMIN_USER_ID:
            bot.send_message(message.chat.id, f"\U0001F6AB Only {USERNAME} can generate codes.", parse_mode='Markdown')
            return

        args = message.text.split()
        if len(args) != 4:
            bot.send_message(message.chat.id, "\U0001F4DD Format: /gen <code> <duration> <max_uses>", parse_mode='Markdown')
            return

        code, duration, max_uses = args[1], args[2], int(args[3])
        expiry_time = datetime.now() + timedelta(days=int(duration[:-1])) if 'd' in duration else datetime.now() + timedelta(hours=int(duration[:-1]))

        codes_collection.insert_one({
            "code": code,
            "expiry_time": expiry_time,
            "max_uses": max_uses,
            "uses": 0
        })

        bot.send_message(message.chat.id, f"\U0001F4AF Code `{code}` generated with duration `{duration}` and max uses `{max_uses}`.", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in /gen: {e}")

# Other Commands (unchanged from your code) ...

# Proxy Update Command
@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, f"\U0001F504 Proxy locked in. We’re untouchable. Bot by {USERNAME}")
    except Exception as e:
        bot.send_message(chat_id, f"\u26A0\uFE0F Proxy config failed: {e}")

def update_proxy():
    proxy_list = []  # Define proxies here
    proxy = random.choice(proxy_list) if proxy_list else None
    if proxy:
        telebot.apihelper.proxy = {'https': proxy}
        logging.info("\U0001F575\uFE0F Proxy shift complete. Surveillance evaded.")

# Main Execution Block
if __name__ == "__main__":
    asyncio.run(main())
