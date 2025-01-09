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

loop = asyncio.get_event_loop()

# Bot Configuration: Set with Authority
TOKEN = 'YOUR TOKEN'
ADMIN_USER_ID = USER ID YOUR
MONGO_URI = 'mongodb+srv://sharp:sharp@sharpx.x82gx.mongodb.net/?retryWrites=true&w=majority&appName=SharpX'
USERNAME = "@VIPMODSXADMIN"  # Immutable username for maximum security

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

async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

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

# Code Redemption Command
@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.send_message(message.chat.id, "\U0001F4DD Format: /redeem <code>", parse_mode='Markdown')
            return

        code = args[1]
        code_data = codes_collection.find_one({"code": code})

        if not code_data:
            bot.send_message(message.chat.id, "\U0001F6AB Invalid code.", parse_mode='Markdown')
            return

        if datetime.now() > code_data["expiry_time"]:
            bot.send_message(message.chat.id, "\U0001F4A5 Code expired.", parse_mode='Markdown')
            return

        if code_data["uses"] >= code_data["max_uses"]:
            bot.send_message(message.chat.id, "\U0001F6D1 Code max uses reached.", parse_mode='Markdown')
            return

        # Increment use count
        codes_collection.update_one({"code": code}, {"$inc": {"uses": 1}})
        bot.send_message(message.chat.id, "\U0001F680 Code redeemed successfully!", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in /redeem: {e}")

# Set Byte Size Command
@bot.message_handler(commands=['byte'])
def set_byte_size(message):
    try:
        if message.from_user.id != ADMIN_USER_ID:
            bot.send_message(message.chat.id, f"\U0001F6AB Only {USERNAME} can set byte size.", parse_mode='Markdown')
            return

        args = message.text.split()
        if len(args) != 2:
            bot.send_message(message.chat.id, "\U0001F4DD Format: /byte <size>", parse_mode='Markdown')
            return

        attack_settings["byte_size"] = int(args[1])
        bot.send_message(message.chat.id, f"\U0001F4AF Byte size set to {attack_settings['byte_size']}.", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in /byte: {e}")

# Set Thread Size Command
@bot.message_handler(commands=['thread'])
def set_thread_size(message):
    try:
        if message.from_user.id != ADMIN_USER_ID:
            bot.send_message(message.chat.id, f"\U0001F6AB Only {USERNAME} can set thread size.", parse_mode='Markdown')
            return

        args = message.text.split()
        if len(args) != 2:
            bot.send_message(message.chat.id, "\U0001F4DD Format: /thread <size>", parse_mode='Markdown')
            return

        attack_settings["thread_size"] = int(args[1])
        bot.send_message(message.chat.id, f"\U0001F4AF Thread size set to {attack_settings['thread_size']}.", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in /thread: {e}")

# Set Attack Time Command
@bot.message_handler(commands=['set_time'])
def set_attack_time(message):
    try:
        if message.from_user.id != ADMIN_USER_ID:
            bot.send_message(message.chat.id, f"\U0001F6AB Only {USERNAME} can set attack time.", parse_mode='Markdown')
            return

        args = message.text.split()
        if len(args) != 2:
            bot.send_message(message.chat.id, "\U0001F4DD Format: /set_time <seconds>", parse_mode='Markdown')
            return

        attack_settings["attack_time"] = int(args[1])
        bot.send_message(message.chat.id, f"\U0001F4AF Attack time set to {attack_settings['attack_time']} seconds.", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in /set_time: {e}")

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

# Other Existing Bot Functions Remain Here...

if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("\U0001F680 Bot is operational and mission-ready.")

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Polling error: {e}")