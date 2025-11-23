import subprocess
import sys
import os

# Tự động cài đặt dependencies nếu thiếu
def install_package(package):
    """Cài đặt package nếu chưa có"""
    try:
        __import__(package)
    except ImportError:
        print(f"Đang cài đặt {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Đã cài đặt {package} thành công!")

# Kiểm tra và cài đặt các package quan trọng
required_packages = {
    'bs4': 'beautifulsoup4',
    'telebot': 'pytelegrambotapi',
    'gtts': 'gtts',
    'pytz': 'pytz',
    'aiohttp': 'aiohttp',
    'requests': 'requests',
    'Crypto': 'pycryptodome',
    'schedule': 'schedule',
    'qrcode': 'qrcode[pil]',
    'jwt': 'PyJWT',
    'protobuf': 'protobuf',
    'httpx': 'httpx',
    'psutil': 'psutil',
    'deep_translator': 'deep-translator',
    'edge_tts': 'edge-tts',
    'urllib3': 'urllib3',
    'yt_dlp': 'yt-dlp'
}

for module_name, package_name in required_packages.items():
    try:
        if module_name == 'bs4':
            from bs4 import BeautifulSoup
        elif module_name == 'Crypto':
            from Crypto.Cipher import AES
        else:
            __import__(module_name)
    except ImportError:
        print(f"Module {module_name} chưa được cài đặt. Đang cài đặt {package_name}...")
        installed = False
        # Thử cài global trước
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Đã cài đặt {package_name} thành công!")
            installed = True
        except Exception:
            # Nếu thất bại, thử cài với --user
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package_name], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Đã cài đặt {package_name} thành công (user mode)!")
                installed = True
            except Exception as e:
                print(f"Lỗi khi cài đặt {package_name}: {e}")
                print(f"Vui lòng chạy: {sys.executable} -m pip3 install {package_name}")
        
        # Nếu đã cài xong, thử import lại
        if installed:
            try:
                if module_name == 'bs4':
                    from bs4 import BeautifulSoup
                elif module_name == 'Crypto':
                    from Crypto.Cipher import AES
                else:
                    __import__(module_name)
                print(f"Đã xác nhận {module_name} hoạt động!")
            except ImportError:
                print(f"CẢNH BÁO: {package_name} đã được cài nhưng vẫn không import được. Có thể cần restart bot.")

import aiohttp
import time
import html
from datetime import datetime, timedelta, date
from threading import Lock
from bs4 import BeautifulSoup
import requests
import subprocess, sys
import re
import random
import json
import os
import threading
import importlib
import sqlite3
import hashlib
import zipfile
import telebot
import tempfile
from gtts import gTTS
from io import BytesIO
from urllib.parse import urljoin, urlparse, urldefrag
from telebot import TeleBot, types  # type: ignore
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import pytz
from datetime import datetime, timedelta
from telebot.types import Message

ALLOWED_GROUP_ID = -1002206366318  # ID BOX
admin_diggory = "nmdc210"
name_bot = "Duck"
zalo = "0965934183"
web = "https://www.mduc.x10.mx/"
facebook = "https://www.facebook.com/nmd210"
allowed_group_id = -1002206366318  # ID BOX
users_keys = {}
freeuser = []
auto_spam_active = False
last_sms_time = {}
allowed_users = []
processes = []
ADMIN_ID = 6836012166  # ID ADMIN
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}
user_cooldowns = {}
share_count = {}
global_lock = Lock()
admin_mode = False
share_log = []
BOT_LINK = 'https://t.me/dungboanhbot'
TOKEN = '8031804112:AAEvuB6jVpEn4EeX31Zwb0TSPSJgBLtQDZE'
bot = TeleBot(TOKEN)
ADMIN_ID = 6836012166 # id admin
admins = {6836012166}
bot_admin_list = {}
cooldown_dict = {}
allowed_users = []
muted_users = {}
running_processes = {}


def get_time_vietnam():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()

    if user_id in last_command_time and current_time - last_command_time[
            user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown -
                             (current_time -
                              last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()


def create_user_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    expiration_time TEXT
                )''')
    conn.commit()
    conn.close()


def TimeStamp():
    now = str(date.today())
    return now


def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.now():
            allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()


###
####
start_time = time.time()
load_users_from_database()


def load_allowed_users():
    try:
        with open('admin_vip.txt', 'r') as file:
            allowed_users = [int(line.strip()) for line in file]
        return set(allowed_users)
    except FileNotFoundError:
        return set()


vip_users = load_allowed_users()


###


@bot.message_handler(commands=['time'])
def handle_time(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    uptime_seconds = int(time.time() - start_time)

    uptime_days, remainder = divmod(uptime_seconds,
                                    86400)  # 1 ngày = 86400 giây
    uptime_hours, remainder = divmod(remainder, 3600)  # 1 giờ = 3600 giây
    uptime_minutes, uptime_seconds = divmod(remainder, 60)  # 1 phút = 60 giây

    bot.reply_to(
        message,
        f'<blockquote>⏰Bot đã hoạt động được: {uptime_days} ngày, {uptime_hours} giờ, {uptime_minutes} phút, {uptime_seconds} giây</blockquote>',
        parse_mode="HTML")


####
#####
video_url = 'https://files.catbox.moe/ivbkxo.MP4'

load_users_from_database()


@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
    admin_id = message.from_user.id
    auto_react_to_command(message)  # <- Thêm dòng này
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'MÁ CÓ PHẢI ADMIN ĐÂU')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.now() + timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    # Gửi video với tiêu đề
    caption_text = (
        f'<blockquote>NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spamvip.</blockquote>'
    )
    bot.send_video(message.chat.id,
                   video_url,
                   caption=caption_text,
                   parse_mode="HTML")


def get_user_status(user_id):
    create_user_table()
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=? AND expiration_time > ?",
              (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    row = c.fetchone()
    conn.close()
    return "VIP" if row else "FREE"


@bot.message_handler(commands=["user"])
def check_user(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_status = get_user_status(user_id)
    auto_react_to_command(message)  # <- Thêm dòng này
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(
        message,
        f"• User ID: {user_id}\n• Username: @{username}\n• Plan: {user_status}\n• Profile By @{username}\n• Timer : {current_time}"
    )

# --- Cấu hình KEY ---
REQUIRE_KEY = True   # Đặt True nếu muốn bắt buộc user nhập key, False nếu free

# Danh sách user đã dùng key
user_keys = {}

def check_user_key(user_id):
    """
    Kiểm tra key của user. 
    Trả về (ok, info)
    """
    if user_id not in user_keys:
        return False, {}
    
    key_info = user_keys[user_id]
    # Ví dụ: {"key": "abc123", "expiration_date": 1695822000}
    if time.time() > key_info.get("expiration_date", 0):
        return False, {}
    
    return True, key_info
    
@bot.message_handler(commands=['listvip'])
def list_vip_users(message):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    auto_react_to_command(message)  # <- Thêm dòng này

    # Lấy danh sách user VIP còn hạn sử dụng
    cursor.execute("SELECT user_id, expiration_time FROM users")
    vip_users = cursor.fetchall()
    conn.close()

    if not vip_users:
        bot.reply_to(message, "Hiện không có user VIP nào trong danh sách.")
        return

    vip_list = "Danh sách VIP:\n"
    now = datetime.now()

    for user_id, expiration_time in vip_users:
        expiration_time = datetime.strptime(expiration_time,
                                            '%Y-%m-%d %H:%M:%S')
        if expiration_time > now:
            vip_list += f"- ID: {user_id} - Hết hạn: {expiration_time}\n"

    bot.send_message(message.chat.id, vip_list, parse_mode="Markdown")


# Kết nối database
def get_db_connection():
    return sqlite3.connect("user_data.db")


# Lệnh để cộng thêm ngày VIP
@bot.message_handler(commands=['congvip'])
def add_vip_days(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message,
                         "Sai cú pháp! Dùng: /congvip <user_id> <days>",
                         parse_mode="Markdown")
            return

        user_id = int(args[1])
        days_to_add = int(args[2])

        conn = get_db_connection()
        cursor = conn.cursor()

        # Lấy ngày hết hạn hiện tại
        cursor.execute("SELECT expiration_time FROM users WHERE user_id = ?",
                       (user_id, ))
        result = cursor.fetchone()

        if result:
            current_expiration = datetime.strptime(result[0],
                                                   "%Y-%m-%d %H:%M:%S")
        else:
            # Nếu user chưa có, mặc định hết hạn từ hôm nay
            current_expiration = datetime.now()

        # Cộng thêm ngày
        new_expiration = current_expiration + timedelta(days=days_to_add)

        # Cập nhật vào database
        cursor.execute(
            "INSERT OR REPLACE INTO users (user_id, expiration_time) VALUES (?, ?)",
            (user_id, new_expiration.strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()

        bot.reply_to(
            message, f"✅ Đã cộng {days_to_add} ngày VIP cho user {user_id}.\n"
            f"📅 Hạn mới: {new_expiration.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")


import time
import random
import string
import requests
import json
import logging
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)

# Globals
LUUKEY_FILE = "luukey.json"
REQUIRE_KEY = False
verified_users = {}  # { user_id: expires_timestamp }
# ======== LƯU XÁC THỰC QUA RESTART ========
VERIFIED_FILE = "verified_users.json"     # a thêm file chỗ này nè 

def load_verified_users():
    """Tải danh sách user đã xác thực (còn hạn) từ file JSON."""
    try:
        with open(VERIFIED_FILE, "r") as f:
            data = json.load(f)
            now = time.time()
            # chỉ giữ user chưa hết hạn
            valid = {int(uid): exp for uid, exp in data.items() if exp > now}
            print(f"[INFO] Loaded {len(valid)} verified users from file.")
            return valid
    except Exception:
        return {}

def save_verified_users():
    """Lưu danh sách user đã xác thực ra file JSON."""
    try:
        with open(VERIFIED_FILE, "w") as f:
            json.dump(verified_users, f)
    except Exception as e:
        print(f"[ERROR] Lỗi lưu verified_users: {e}")

# ✅ Load khi bot khởi động
verified_users = load_verified_users()


# ---------- Utils ----------
def load_keys():
    try:
        with open(LUUKEY_FILE, "r") as f:
            data = json.load(f)
            # Loại bỏ các key quá hạn
            now = time.time()
            valid_data = {int(k): v for k, v in data.items() if v.get("expires", 0) > now}
            return valid_data
    except Exception:
        return {}

def save_keys(data):
    try:
        with open(LUUKEY_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error("Lỗi lưu key: %s", e)

stored_keys = load_keys()  # load khi bot start

def generate_key():
    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"mduc×thl-{rand_str}"

def check_user_key(user_id):
    try:
        uid = int(user_id)
    except:
        return False, {"reason": "user_id không hợp lệ"}

    exp = verified_users.get(uid)
    if not exp:
        return False, {"reason": "User chưa xác thực"}
    if time.time() > exp:
        verified_users.pop(uid, None)
        return False, {"reason": "Key xác thực đã hết hạn"}
    return True, {"reason": "OK", "expires": exp}

# =================== LỆNH /KEY ===================
@bot.message_handler(commands=['off'])
def bot_off(message):
    global bot_active
    if message.from_user.id in admins:
        bot_active = False
        bot.reply_to(message, 'Bot đã được tắt.')
    else:
        bot.reply_to(message, 'Bạn không có quyền thực hiện thao tác này.')


@bot.message_handler(commands=['on'])
def bot_on(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    global bot_active
    if message.from_user.id in admins:
        bot_active = True
        bot.reply_to(message, 'Bot đã được bật.')
    else:
        bot.reply_to(message, 'Bạn không có quyền thực hiện thao tác này.')
        
        
@bot.message_handler(commands=['fb'])
def send_facebook_info(message):
    chat_id = message.chat.id
    message_id = message.message_id

    waiting = bot.reply_to(message, "🔍")
    user_input = message.text.split(maxsplit=1)

    if len(user_input) < 2:
        bot.send_message(chat_id, "❌ Vui lòng nhập UID hoặc Link sau lệnh /fb\n\n💬 Ví Dụ: <code>/fb 61574395204757</code> hoặc <code>/fb https://facebook.com/zuck</code>", parse_mode="HTML")
        bot.delete_message(chat_id, waiting.message_id)
        return

    fb_input = user_input[1].strip()

    if fb_input.isdigit():
        fb_id = fb_input
    else:
        fb_link = fb_input
        if not fb_link.startswith("http"):
            fb_link = "https://" + fb_link

        convert_api = f"https://offvnx.x10.bz/api/convertID.php?url={fb_link}"
        try:
            convert_res = requests.get(convert_api)
            if convert_res.status_code == 200:
                convert_data = convert_res.json()
                fb_id = str(convert_data.get("id", ""))
                if not fb_id.isdigit():
                    bot.send_message(chat_id, "❌ Không thể lấy UID từ link Facebook này! Vui lòng kiểm tra lại.")
                    bot.delete_message(chat_id, waiting.message_id)
                    return
            else:
                bot.send_message(chat_id, "❌ Lỗi khi kết nối API lấy UID.")
                bot.delete_message(chat_id, waiting.message_id)
                return
        except Exception as e:
            bot.send_message(chat_id, f"❌ Lỗi khi lấy UID từ link: {e}")
            bot.delete_message(chat_id, waiting.message_id)
            return

    api_url = f"https://offvnx.x10.bz/api/fb.php?id={fb_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            data = response.json().get("result", {})

            if not isinstance(data, dict):
                bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, Có Thể Bạn Đã Nhập Sai Định Dạng")
                bot.delete_message(chat_id, waiting.message_id)
                return

            name = data.get("name", "Không công khai")
            username = data.get("username", "Chưa thiết lập")
            profile_id = data.get("id", "Chưa thiết lập")
            link = data.get("link", "https://www.facebook.com/")
            is_verified = data.get("is_verified", False)
            picture = data.get("picture", {}).get("data", {}).get("url", "")
            is_silhouette = data.get("picture", {}).get("data", {}).get("is_silhouette", True)
            created_time = data.get("created_time", "Không công khai")
            about = data.get("about", "Không công khai")
            locale = data.get("locale", "Không công khai")
            gender = data.get("gender", "Không công khai").capitalize()
            hometown = data.get("hometown", {}).get("name", "Không công khai")
            location = data.get("location", {}).get("name", "Không công khai")
            updated_time = data.get("updated_time", "Không công khai")
            timezone = data.get("timezone", "Không công khai")
            work = data.get("work", [])
            cover_photo = data.get("cover", {}).get("source", "")
            followers = data.get("followers", "Không công khai")
            following = data.get("following", "Không rõ số lượng đang theo dõi")
            relationship = data.get("relationship_status", "Không công khai")
            significant_other = data.get("significant_other", {})
            significant_other_name = significant_other.get("name", "Không công khai")
            significant_other_id = significant_other.get("id", "Không công khai")
            flag = data.get("country_flag", "")
            relationship_icon_text = data.get("relationship_status", "❓ Không công khai")

            work_info = ""
            if work:
                for job in work:
                    position = job.get("position", {}).get("name", "")
                    employer = job.get("employer", {}).get("name", "")
                    work_info += f"\n│ -> Làm việc tại {position} <a href='https://facebook.com/{username}'>{employer}</a>"
            else:
                work_info = "Không công khai"

            education_info = ""
            education = data.get("education", [])
            if education:
                for edu in education:
                    school = edu.get("school", {}).get("name", "Không công khai")
                    education_info += f"\n│ -> Học {edu.get('concentration', [{'name': ''}])[0]['name']} tại <a href='https://facebook.com/{username}'>{school}</a>"
            else:
                education_info = "Không công khai"

            verification_status = "Đã Xác Minh ✅" if is_verified else "Chưa xác minh ❌"

            significant_other_line = ""
            if significant_other_id not in ["Không công khai", "Chưa thiết lập", None, ""]:
                significant_other_line = (
                    f"│ -> 💍 Đã kết hôn với: <a href='https://facebook.com/{significant_other_id}'>{significant_other_name}</a>\n"
                    f"│ -> 🔗 Link UID: <code>https://facebook.com/{significant_other_id}</code>"
                )

            cover_photo_line = f"│ 𝗖𝗼𝘃𝗲𝗿 𝗣𝗵𝗼𝘁𝗼: <a href='{cover_photo}'>Xem ảnh bìa</a>" if cover_photo else "│ 𝗖𝗼𝘃𝗲𝗿 𝗣𝗵𝗼𝘁𝗼: Không có ảnh bìa ❌"
            profile_photo_line = f"│ 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗣𝗵𝗼𝘁𝗼: <a href='{picture}'>Xem ảnh đại diện</a>" if picture and not is_silhouette else "│ 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗣𝗵𝗼𝘁𝗼: Không có ảnh đại diện ❌"

            fb_info = f"""
<blockquote>╭─────────────⭓
│ 𝗡𝗮𝗺𝗲: <a href='{picture}'>{name}</a>
│ 𝗨𝗜𝗗: <a href='https://facebook.com/{profile_id}'>{profile_id}</a>
│ 𝗨𝘀𝗲𝗿 𝗡𝗮𝗺𝗲: <a href='https://facebook.com/{username}'>{username}</a>
{cover_photo_line}
{profile_photo_line}
│ 𝗟𝗶𝗻𝗸: {link}
│ 𝗕𝗶𝗿𝘁𝗵𝗱𝗮𝘆: {data.get("birthday", "Không hiển thị ngày sinh")}
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀: <a href='https://facebook.com/{profile_id}'>{followers}</a> Người theo dõi
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴: {following}
│ 𝗗𝗮𝘁𝗲 𝗖𝗿𝗲𝗮𝘁𝗲𝗱: {created_time}
│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻: {verification_status}
│ 𝗦𝘁𝗮𝘁𝘂𝘀: {relationship_icon_text}
{significant_other_line}
│ 𝗕𝗶𝗼: {about}
│ 𝗚𝗲𝗻𝗱𝗲𝗿: {gender}
│ 𝗛𝗼𝗺𝗲𝘁𝗼𝘄𝗻: {hometown}
│ 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻: {location}
│ 𝗪𝗼𝗿𝗸: {work_info}
│ 𝗘𝗱𝘂𝗰𝗮𝘁𝗶𝗼𝗻: {education_info}
│ 𝗔𝗯𝗼𝘂𝘁𝘀: {data.get("quotes", "Không có trích dẫn")}
├─────────────⭔
│ 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: {flag}
│ 𝗧𝗶𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲: {updated_time}
╰─────────────⭓
</blockquote>
            """
            markup = InlineKeyboardMarkup()
            callback_data = f"delete_{chat_id}_{message.from_user.id}"
            delete_button = InlineKeyboardButton(text="🗑️ Xoá Tin Nhắn", callback_data=callback_data)
            markup.add(delete_button)

            bot.send_message(chat_id, fb_info, parse_mode='HTML', reply_markup=markup)
            bot.delete_message(chat_id, waiting.message_id)

        except Exception as e:
            bot.send_message(chat_id, f"Đã xảy ra lỗi khi xử lý dữ liệu: {str(e)}")
            bot.delete_message(chat_id, waiting.message_id)
    else:
        bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, Có Thể Bạn Đã Nhập Sai Định Dạng")
        bot.delete_message(chat_id, waiting.message_id)

    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Lỗi xóa lệnh: {e}")

# 👉 Xử lý callback xoá tin nhắn
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def handle_delete_callback(call):
    try:
        _, msg_chat_id, msg_user_id = call.data.split("_")
        if str(call.from_user.id) != msg_user_id:
            bot.answer_callback_query(call.id, "❌ Bạn không có quyền xoá tin nhắn này.", show_alert=True)
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.answer_callback_query(call.id, f"Lỗi: {e}", show_alert=True)

# ========================
# HÀM DÙNG CHUNG
# ========================
def safe_get(data):
    return data if isinstance(data, dict) else {}

def ts_to_date(ts):
    try:
        if ts is None:
            return ""
        return datetime.fromtimestamp(int(ts)).strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ""

def get_country_flag(region_code):
    try:
        if not region_code:
            return ""
        region_code = region_code.upper().strip()
        country_map = {
            "VN": "Việt Nam 🇻🇳", "SG": "Singapore 🇸🇬", "ID": "Indonesia 🇮🇩",
            "TH": "Thái Lan 🇹🇭", "PH": "Philippines 🇵🇭", "MY": "Malaysia 🇲🇾",
            "KH": "Campuchia 🇰🇭", "LA": "Lào 🇱🇦", "MM": "Myanmar 🇲🇲",
            "IN": "Ấn Độ 🇮🇳", "BD": "Bangladesh 🇧🇩", "BR": "Brazil 🇧🇷",
            "US": "Hoa Kỳ 🇺🇸", "KR": "Hàn Quốc 🇰🇷", "JP": "Nhật Bản 🇯🇵",
            "CN": "Trung Quốc 🇨🇳", "TW": "Đài Loan 🇹🇼", "HK": "Hồng Kông 🇭🇰",
        }
        if region_code in country_map:
            return country_map[region_code]
        if len(region_code) == 2:
            flag = chr(ord(region_code[0]) + 127397) + chr(ord(region_code[1]) + 127397)
            return f"{region_code} {flag}"
        return region_code
    except:
        return region_code

# ========================
import telebot
import requests
from io import BytesIO
from datetime import datetime
from html import escape   # <--- thêm dòng này
import time

OUTFIT_API_URL = "https://ffoutfitapis.vercel.app/outfit-image?uid={uid}&region={region}&key=99day"
PLAYER_INFO_API = "https://ffinfo-mu.vercel.app/player-info?uid={uid}&region={region}"
WISHLIST_API_URL = "https://ffwishlistapis.vercel.app/wish?uid={uid}&region={region}"
EVENTS_API_URL = "https://narayan-event.vercel.app/event?region={region}"
REGION_API_URL = 'https://danger-region-check.vercel.app/region?uid={uid}&key=DANGERxREGION'
BANCHECK_API_URL = 'https://ff.garena.com/api/antihack/check_banned?lang=en&uid={uid}'


# ================= BOT COMMANDS =================

@bot.message_handler(commands=['bancheck'])
def bancheck_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Cách dùng: /bancheck <uid>\nVí dụ: /bancheck 12345678")
            return
            
        uid = parts[1]
        if not is_valid_uid(uid):
            bot.reply_to(message, "UID không hợp lệ! UID phải có 8-11 chữ số.", parse_mode="HTML")
            return
            
        processing_msg = bot.reply_to(message, "Đang kiểm tra trạng thái cấm...", parse_mode="HTML")
        
        result = check_ban_status(uid, show_nickname=True)
        formatted_result = f"""────────────────────
{result}
────────────────────
🔰 Developer : @nmdc210"""
        bot.edit_message_text(
            formatted_result,
            processing_msg.chat.id,
            processing_msg.message_id,
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ LỖI: {str(e)}")


from datetime import datetime
from io import BytesIO
import requests
import time

# Chỉ hỗ trợ 2 region
VALID_REGIONS = ["vn", "sg"]

def convert_timestamp(ts):
    try:
        ts = int(ts)
        # Nếu timestamp > 1e12, coi là mili giây, chia 1000
        if ts > 1e12:
            ts = ts // 1000
        dt = datetime.fromtimestamp(ts)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
        return date_str, time_str
    except:
        return "ɴ/ᴀ", "ɴ/ᴀ"



@bot.message_handler(commands=['loveqr'])
def create_love_qr(message):
    user_id = message.from_user.id  # thêm user_id để check key

    # 🔑 Kiểm tra key
    if REQUIRE_KEY:
        try:
            ok, info = check_user_key(user_id)
        except Exception:
            ok, info = False, {}
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # Xử lý text nhập vào
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        return bot.reply_to(
            message,
            "<blockquote>💘 Cách dùng:</blockquote>\n<pre>/loveqr Light Love Suu💖</pre>",
            parse_mode="HTML"
        )

    user_text = args[1].strip()

    # Tạo payload base64
    payload = {
        "t": [user_text],
        "a": "nnca"
    }
    b64_data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    final_url = f"https://taoanhdep.com/love/?b={b64_data}"

    # Tạo QR
    qr = qrcode.make(final_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Gửi QR kèm caption
    caption = (
        "<blockquote>"
        f"<code>💗 Success Reg Qrcode Love Text: {user_text}</code>\n\n"
        f"🌐 <a href='{final_url}'> {final_url}</a>"
        "</blockquote>"
    )

    bot.send_photo(message.chat.id, photo=buffer, caption=caption, parse_mode="HTML")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    chat_id = message.chat.id
    member_count = bot.get_chat_members_count(chat_id)

    for new_member in message.new_chat_members:
        user_id = new_member.id
        username = new_member.username
        first_name = new_member.first_name or "Người dùng"

        # Xử lý hiển thị tên người dùng
        if username:
            requester = f'@{username}'
        else:
            requester = f'<a href="tg://user?id={user_id}">{first_name}</a>'

        # Tin nhắn Welcome
        welcome_text = f"""
❖ 🎉 <b>Welcome</b> 🎉 ❖

<blockquote><b>Xin Chào</b> 👋! {requester}</blockquote>
<blockquote>➩ <b>Đã Tham Gia Nhóm:</b> {html.escape(message.chat.title)}</blockquote>
<blockquote>➩ <b>Số thành viên hiện tại:</b> {member_count}</blockquote>

▣ Dùng <b>/help</b> để xem tất cả lệnh của bot
"""

        # Inline buttons
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("👑 Admin", url="https://t.me/nmdc210"),
            types.InlineKeyboardButton("📢 Kênh thông báo", url="https://t.me/thlcte")
        )
        keyboard.add(
            types.InlineKeyboardButton("💬 Nhóm chat", url="https://t.me/thlcte"),
        )

        # Gửi Welcome kèm video
        video_url = "https://i.imgur.com/SRFiXrt.mp4"
        bot.send_video(
            chat_id,
            video_url,
            caption=welcome_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    import pytz
    from datetime import datetime

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    vn_time = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))

    bot.send_message(
        message.chat.id,
        f"""
<b>{name_bot}</b>

<b>Thời gian:</b> {vn_time.strftime('%H:%M:%S')}
<b>Ngày:</b> {vn_time.strftime('%d/%m/%Y')}
<b>Xin chào:</b> <a href='tg://user?id={user_id}'>{user_name}</a>

<b>Lệnh cơ bản:</b>
- /start, /help: Hiển thị danh sách lệnh
- /admin: Trung tâm điều khiển admin
- /user: Kiểm tra trạng thái tài khoản
- /fb: Tra cứu thông tin Facebook
- /thoitiet: Xem dự báo thời tiết
- /voice: Chuyển văn bản thành giọng nói
- /dich: Dịch ngôn ngữ
- /loveqr: Tạo mã QR tình yêu
- /scl: Nghe nhạc trên scl 
- /taoanh: tạo ảnh bằng Ai

<b>Lệnh spam:</b>
- /sms, /spam: Spam cơ bản
- /spamvip: Spam tốc độ cao
- /stop [số]: Dừng spam
- /muavip: Nâng cấp VIP

<b>Lệnh admin:</b>
- /add: Thêm key hoặc quyền
- /bansdt: Chặn số điện thoại

<b>Ghi chú:</b>
Bot hoạt động tự động, dữ liệu được xử lý an toàn.
        """,
        parse_mode="HTML"
    )

@bot.message_handler(commands=['admin'])
def diggory(message):
    username = message.from_user.username or "Người dùng"
    bot.reply_to(
        message,
        f"""
<b>{name_bot} - Trung tâm điều khiển</b>

<b>Người dùng:</b> @{username}
<b>Hệ thống:</b> {name_bot}
<b>Zalo:</b> {zalo}
<b>Website:</b> {web}
<b>Telegram admin:</b> @{admin_diggory}

Liên hệ admin để được hỗ trợ nhanh nhất.
        """,
        parse_mode="HTML"
    )


blacklist = {}
last_usage = {}
SPAM_PROCESSES = {}
active_processes = {}  # Lưu PID theo số điện thoại

def hide_phone_number(phone_number):
    if len(phone_number) < 8:
        return phone_number
    return phone_number[:4] + "****" + phone_number[-2:]

@bot.message_handler(commands=['spam'])
def spam(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    # Kiểm tra key NGAY LÚC ĐẦU để tránh tốn tài nguyên nếu chưa có key
    if REQUIRE_KEY:
        try:
            ok, info = check_user_key(user_id)
        except Exception:
            ok, info = False, {}
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # Gọi phản ứng tự động (nếu có)
    try:
        auto_react_to_command(message)
    except Exception:
        pass

    # Xóa tin nhắn lệnh của user (nếu bot có quyền)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass  # Bỏ qua nếu không xóa được

    # --- tiếp tục phần xử lý spam như bạn muốn ---
    # (ví dụ: phân tích args, kiểm tra rate limit, blacklist, chạy subprocess, v.v.)
    # ====== Phần xử lý spam ======
    processing_msg = None
    try:
        processing_msg = bot.send_message(
            chat_id,
            f"⏳ <a href='tg://user?id={user_id}'>{user_name}</a>, đang xử lý SMS...",
            parse_mode="HTML"
        )
    except Exception:
        # Nếu gửi message ban đầu fail thì vẫn tiếp tục, nhưng không thể edit sau này
        processing_msg = None

    # Tạo keyboard
    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/nmdc210')
    keyboard.add(url_button1)

    # Lấy tham số từ message
    params = message.text.split()[1:]
    if len(params) != 2:
        text = "/spam SĐT Số lần\nVD: /spam 0123456789 5"
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    sdt, count = params

    if not count.isdigit():
        text = "Số lần spam không hợp lệ. Vui lòng chỉ nhập số."
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    count = int(count)

    if count > 5:
        text = "<blockquote>Lệnh này tối đa là 5 lần !!!</blockquote>"
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id, parse_mode="HTML")
        else:
            bot.send_message(chat_id, text, parse_mode="HTML")
        return

    if sdt in blacklist:
        text = f"🚫 Số điện thoại {sdt} đã bị cấm spam."
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 60:
        wait_time = int(60 - (current_time - last_usage[user_id]))
        text = f"⏳ Vui lòng đợi {wait_time} giây trước khi dùng lệnh lại."
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    last_usage[user_id] = current_time
    hidden_sdt = hide_phone_number(sdt)

    # Gửi video xác nhận spam
    video_url = "https://files.catbox.moe/wri854.mp4"
    try:
        bot.send_video(
            chat_id,
            video_url,
            caption=(
                f"<blockquote><b>┌──⭓ SPAM SMS💳</b>\n"
                f"<b>│</b> 🚀 <b>Attack Sent Successfully</b>\n"
                f"<b>│</b> 💳 <b>Plan Free:</b> Min 1 | Max 5\n"
                f"<b>│</b> 📞 <b>Phone:</b> {hidden_sdt}\n"
                f"<b>│</b> ⚔️ <b>Attack By:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
                f"<b>│</b> 🔗 <b>API:</b> 1x\n"
                f"<b>│</b> ⏳ <b>Delay:</b> 20s\n"
                f"<b>│</b> 📎 <b>Vòng Lặp:</b> <code>{count}</code>\n"
                f"<b>└────────────⭓</b></blockquote>"
                f"<pre>Dừng: /stop SĐT\n/stop {sdt}</pre>"
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        # Nếu gửi video thất bại, vẫn tiếp tục chạy script (tùy bạn)
        try:
            bot.send_message(chat_id, f"⚠️ Không thể gửi video xác nhận: {e}")
        except Exception:
            pass

    # --- CHẠY SCRIPT test1.py ---
    script_filename = "test1.py"
    try:
        if not os.path.isfile(script_filename):
            bot.send_message(chat_id, "⚠️ Không tìm thấy file script `test1.py`.")
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy script với tham số sdt và count
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        # Lưu PID để dùng /stop
        active_processes[sdt] = process.pid
    except Exception as e:
        bot.send_message(chat_id, f"❌ Lỗi chạy script: {str(e)}")
        


@bot.message_handler(commands=['sms'])
def sms(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    # Kiểm tra key NGAY LÚC ĐẦU để tránh tốn tài nguyên
    if REQUIRE_KEY:
        ok, info = check_user_key(user_id)
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # Phản ứng tự động (nếu có)
    try:
        auto_react_to_command(message)
    except Exception:
        pass

    # Xóa lệnh người dùng (nếu có quyền)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

    # Thông báo đang xử lý
    processing_msg = bot.send_message(
        chat_id,
        f"⏳ <a href='tg://user?id={user_id}'>{user_name}</a>, đang xử lý SMS...",
        parse_mode="HTML"
    )

    # Inline keyboard (quảng cáo / buy vip)
    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/nmdc210')
    keyboard.add(url_button1)

    # Lấy tham số
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.edit_message_text(
            "/sms SĐT số lần\nVD: /sms 0123456789 5\nSĐT Viết Liền Nhau.",
            chat_id,
            processing_msg.message_id
        )
        return

    sdt, count = params

    if not count.isdigit():
        bot.edit_message_text(
            "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.",
            chat_id,
            processing_msg.message_id
        )
        return

    count = int(count)

    if count > 5:
        bot.edit_message_text(
            "<blockquote>Lệnh này tối đa là 5 lần !!!</blockquote>",
            chat_id,
            processing_msg.message_id,
            parse_mode="HTML"
        )
        return

    if sdt in blacklist:
        bot.edit_message_text(
            f"🚫 Số điện thoại {sdt} đã bị cấm spam.",
            chat_id,
            processing_msg.message_id
        )
        return

    # Rate limit per user (60s)
    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 60:
        wait_time = int(60 - (current_time - last_usage[user_id]))
        bot.edit_message_text(
            f"⏳ Vui lòng đợi {wait_time} giây trước khi dùng lệnh lại.",
            chat_id,
            processing_msg.message_id
        )
        return

    last_usage[user_id] = current_time
    hidden_sdt = hide_phone_number(sdt)

    # Gửi thông báo (video + nội dung)
    video_url = "https://files.catbox.moe/wri854.mp4"
    try:
        sent_video = bot.send_video(
            chat_id,
            video_url,
            caption=(
                f"<blockquote><b>┌──⭓ SPAM SMS FREE💳</b>\n"
                f"<b>│</b> 🚀 <b>Attack Sent Successfully</b>\n"
                f"<b>│</b> 💳 <b>Plan Free:</b> Min 1 | Max 5\n"
                f"<b>│</b> 📞 <b>Phone:</b> {hidden_sdt}\n"
                f"<b>│</b> ⚔️ <b>Attack By:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
                f"<b>│</b> 🔗 <b>Api:</b> 1x (MAX)\n"
                f"<b>│</b> ⏳ <b>Delay:</b> 20s\n"
                f"<b>│</b> 📎 <b>Vòng Lặp:</b> <code>{count}</code>\n"
                f"<b>└────────────⭓</b></blockquote>\n"
                f"<pre>Dừng: /stop SĐT\n/stop 0987654321</pre>"
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception:
        # Nếu không gửi được video thì chỉ edit tin nhắn processing
        try:
            bot.edit_message_text(
                f"✅ Đã gửi lệnh spam cho {hidden_sdt} (vòng lặp: {count})",
                chat_id,
                processing_msg.message_id
            )
        except Exception:
            pass

    # Chạy script spam SMS (tạo temp file và chạy subprocess)
    script_filename = "cc.py"
    try:
        if not os.path.isfile(script_filename):
            bot.edit_message_text("Không tìm thấy file script. Vui lòng kiểm tra lại.", chat_id, processing_msg.message_id)
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Khởi chạy subprocess (không chặn)
        process = subprocess.Popen([sys.executable, temp_file_path, sdt, str(count)])

        # Bạn có thể lưu process.pid nếu cần dừng sau bằng /stop
        running_processes[user_id] = {
            "pid": process.pid,
            "temp_file": temp_file_path,
            "target": sdt
        }

    except FileNotFoundError:
        bot.edit_message_text("Không tìm thấy file.", chat_id, processing_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Lỗi xảy ra: {str(e)}", chat_id, processing_msg.message_id)
        

active_spams = {}

@bot.message_handler(commands=['stop'])
def stop(message):
    params = message.text.split()[1:]
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(params) != 1:
        bot.reply_to(message, "🔴 Dùng lệnh: /stop SĐT\nVD: /stop 0123456789")
        return

    sdt = params[0]

    if sdt not in active_processes:
        bot.reply_to(message, f"❌ Không có tiến trình nào đang chạy cho SĐT {sdt}.")
        return

    try:
        os.kill(active_processes[sdt], 9)  # Dừng process
        del active_processes[sdt]  # Xóa khỏi danh sách
        bot.reply_to(message, f"🛑 Đã dừng spam cho {sdt}.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi dừng spam: {e}")





blacklist = [
    "112", "113", "114", "115", "116", "117", "118", "119", "1",
    "2", "3", "4"
]


# Xử lý lệnh /spamvip
def is_valid_phone(phone):
    return bool(re.fullmatch(r"0\d{9}", phone))
@bot.message_handler(commands=['spamvip'])
def spamvip(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id
    auto_react_to_command(message)  # <- Thêm dòng này

    if user_id not in allowed_users:
        bot.reply_to(message, 'Mua Vip Liên Hệ ADMIN @nmdc210')
        return

    # Xóa tin nhắn của user
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

    # Bot gửi thông báo "Đang xử lý..."
    processing_msg = bot.send_message(chat_id, f"⏳ <a href='tg://user?id={user_id}'>{user_name}</a>, đang xử lý SMS...", parse_mode="HTML")

    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/nmdc210')
    keyboard.add(url_button1)


    params = message.text.split()[1:]
    if len(params) != 2:
        bot.edit_message_text("/spamvip SĐT Số_lần\nVD: /spamvip 0123456789 1000", chat_id, processing_msg.message_id)
        return

    sdt, count = params

    if not count.isdigit():
        bot.edit_message_text("Số lần spam không hợp lệ. Vui lòng chỉ nhập số.", chat_id, processing_msg.message_id)
        return

    count = int(count)

    if count > 1000:
        bot.edit_message_text("<blockquote>Lệnh này tối đa là 1000 lần !!!</blockquote>", chat_id, processing_msg.message_id, parse_mode="HTML")
        return

    if sdt in blacklist:
        bot.edit_message_text(f"🚫 Số điện thoại {sdt} đã bị cấm spam.", chat_id, processing_msg.message_id)
        return

    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 20:
        wait_time = int(20 - (current_time - last_usage[user_id]))
        bot.edit_message_text(f"⏳ Vui lòng đợi {wait_time} giây trước khi dùng lệnh lại.", chat_id, processing_msg.message_id)
        return

    last_usage[user_id] = current_time
    hidden_sdt = hide_phone_number(sdt)

    # Cập nhật tin nhắn thành kết quả spam
    video_url = "https://files.catbox.moe/ojg5t7.mp4"
    sent_video = bot.send_video(
        chat_id, 
        video_url, processing_msg.message_id,
        caption=(
            f"<blockquote><b>┌──⭓ SPAM SMS VIP💎🚀</b>\n"
            f"<b>│</b> 🚀 <b>Attack Sent Successfully</b>\n"
            f"<b>│</b> 💳 <b>Plan Vip:</b> Min 1 | Max 1000\n"
            f"<b>│</b> 📞 <b>Phone:</b> {hidden_sdt}\n"
            f"<b>│</b> ⚔️ <b>Attack By:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
            f"<b>│</b> 🔗 <b>Api:</b> 10x (MAX)\n"
            f"<b>│</b> ⏳ <b>Delay:</b> 20s\n"
            f"<b>│</b> 📎 <b>Vòng Lặp:</b> <code>{count}</code>\n"
            f"<b>└────────────⭓</b></blockquote>\n"
            f"<pre>Dừng: /stopvip SĐT\n/stopvip 0987654321\nCÁM ƠN MN ỦNG HỘ VIP NHÉ.</pre>"
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )

    # Chạy script spam SMS
    script_filename = "test1.py"
    try:
        if not os.path.isfile(script_filename):
            bot.edit_message_text("Không tìm thấy file script. Vui lòng kiểm tra lại.", chat_id, processing_msg.message_id)
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        # Lưu PID và user_id vào active_processes
        active_processes[sdt] = {'pid': process.pid, 'user_id': user_id}
    except FileNotFoundError:
        bot.edit_message_text("Không tìm thấy file.", chat_id, processing_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Lỗi: {e}", chat_id, processing_msg.message_id)


active_spams = {}



@bot.message_handler(commands=['stopvip'])
def stopvip(message):
    user_id = message.from_user.id
    auto_react_to_command(message)  # <- Thêm dòng này
    if user_id not in allowed_users:
        bot.reply_to(message, 'Mua Vip Liên Hệ ADMIN @nmdc210')
        return
    params = message.text.split()[1:]
    if len(params) != 1:
        bot.reply_to(message, "🔴 Dùng lệnh: /stopvip SĐT\nVD: /stopvip 0123456789")
        return

    sdt = params[0]
    user_id = message.from_user.id  # Lấy user_id của người gửi lệnh

    # Kiểm tra xem tiến trình cho số điện thoại có tồn tại không
    if sdt not in active_processes:
        bot.reply_to(message, f"❌ Không có tiến trình nào đang chạy cho SĐT {sdt}.")
        return

    # Kiểm tra xem người dừng có phải là người đã kích hoạt spam không
    if active_processes[sdt].get('user_id') != user_id:
        bot.reply_to(message, f"⚠️ Bạn không có quyền dừng tiến trình spam cho {sdt}. Chỉ người khởi tạo mới có thể dừng.")
        return

    try:
        os.kill(active_processes[sdt]['pid'], 9)  # Dừng process
        del active_processes[sdt]  # Xóa khỏi danh sách
        bot.reply_to(message, f"🛑 Đã dừng spam cho {sdt}.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi dừng spam: {e}")




# Danh sách blacklist (có thể lưu vào file/database)
BLACKLIST_FILE = "blacklist.json"

# Regex kiểm tra số điện thoại hợp lệ (10 số, bắt đầu bằng 0)
PHONE_REGEX = re.compile(r"^0\d{9}$")

def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_blacklist():
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(list(blacklist), f)

blacklist = load_blacklist()

# Lệnh /bansdt <số điện thoại>
@bot.message_handler(commands=['bansdt'])
def add_blacklist(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.from_user.id == ADMIN_ID:
        try:
            phone_number = message.text.split()[1]
            if PHONE_REGEX.match(phone_number):
                blacklist.add(phone_number)
                save_blacklist()
                bot.reply_to(message, f"Đã thêm {phone_number} vào blacklist.")
            else:
                bot.reply_to(message, "Số điện thoại không hợp lệ! (Yêu cầu 10 số, bắt đầu bằng 0).")
        except IndexError:
            bot.reply_to(message, "Vui lòng nhập số điện thoại!")
    else:
        bot.reply_to(message, "Ủa Alo Mày Phải Admin Đâu!")

# Lệnh /unbansdt <số điện thoại>
@bot.message_handler(commands=['unbansdt'])
def remove_blacklist(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.from_user.id == ADMIN_ID:
        try:
            phone_number = message.text.split()[1]
            if phone_number in blacklist:
                blacklist.remove(phone_number)
                save_blacklist()
                bot.reply_to(message, f"Đã xóa {phone_number} khỏi blacklist.")
            else:
                bot.reply_to(message, f"Số {phone_number} không có trong blacklist.")
        except IndexError:
            bot.reply_to(message, "Vui lòng nhập số điện thoại!")
    else:
        bot.reply_to(message, "Nói Roi Mà Mày Làm Gì Là Admin!")

# Xử lý tin nhắn chứa số điện thoại hợp lệ
@bot.message_handler(func=lambda message: message.text and PHONE_REGEX.match(message.text.strip()))
def check_blacklist(message):
    phone_number = message.text.strip()
    if phone_number in blacklist:
        bot.reply_to(message, "Số điện thoại này đã bị chặn!")


ADMIN_NAME = "nmdc210"


@bot.message_handler(commands=['ad'])
def send_admin_info(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    bot.send_message(message.chat.id,
                     f"Only One => Is : {ADMIN_NAME}\nID: `{ADMIN_ID}`",
                     parse_mode='Markdown')

ADMIN_NAME = "nmdc210"

@bot.message_handler(commands=['id'])
def get_user_id(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(message.text.split()) == 1:
        user_id = message.from_user.id
        bot.reply_to(message,
                     f"ID của bạn là: `{user_id}`",
                     parse_mode='Markdown')
    else:
        username = message.text.split('@')[-1].strip()
        try:
            user = bot.get_chat(
                username)  # Lấy thông tin người dùng từ username
            bot.reply_to(message,
                         f"ID của {user.first_name} là: `{user.id}`",
                         parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, "Không tìm thấy người dùng có username này.")


@bot.message_handler(commands=['info'])
def send_info(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.reply_to_message:
        users = [message.reply_to_message.from_user]
    else:
        args = message.text.split()[1:]
        users = [message.from_user]

        if args:
            users = []
            for arg in args:
                try:
                    user_id = int(arg) if arg.isdigit() else arg
                    user = bot.get_chat(user_id)
                    users.append(user)
                except Exception:
                    return

    for user in users:
        try:
            bio = bot.get_chat(user.id).bio if hasattr(bot.get_chat(user.id), 'bio') else "Không có hoặc không thể lấy được"
        except Exception:
            bio = "Không Có hoặc không thể lấy được"


        full_name = f"{user.first_name} {user.last_name or ''}".strip()
        link_name = f'<a href="tg://user?id={user.id}">{full_name}</a>'

        status = "Không xác định"
        if message.chat.type in ['group', 'supergroup']:
            try:
                member = bot.get_chat_member(message.chat.id, user.id)
                status = member.status
                if status == 'creator':
                    status = "Người Tạo Nhóm"
                elif status == 'administrator':
                    status = "Quản Trị Viên"
                elif status == 'member':
                    status = "Thành Viên"
                elif status == 'left':
                    status = "Đã Rời Nhóm"
                elif status == 'kicked':
                    status = "Bị Đuổi Khỏi Nhóm"
            except Exception:
                status = "Không thể xác định trạng thái"

        info_text = (
            f"<b>👤 Thông Tin Người Dùng:</b>\n"
            f"<b>┌ UID:</b> <code>{user.id}</code>\n"
            f"<b>├ Tên:</b> {link_name}\n"
            f"<b>├ Username:</b> @{user.username if user.username else 'Không có'}\n"
            f"<b>├ Ngôn Ngữ:</b> {getattr(user, 'language_code', 'Không xác định')}\n"
            f"<b>├ Trạng Thái:</b> {status}\n"
            f"<b>└ Bio:</b> {bio}\n"
        )

        photos = bot.get_user_profile_photos(user.id, limit=1)
        if photos.photos:
            photo_file_id = photos.photos[0][-1].file_id
            bot.send_photo(message.chat.id, photo_file_id, caption=info_text, parse_mode="HTML",  reply_to_message_id=message.message_id)
        else:
            bot.reply_to(message, info_text, parse_mode="HTML")


@bot.message_handler(commands=['ID'])
def handle_id_command(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    chat_id = message.chat.id
    bot.reply_to(message, f"ID của nhóm này là: {chat_id}")


####################
import time


def restart_program():
    """Khởi động lại script chính và môi trường chạy."""
    python = sys.executable
    script = sys.argv[0]
    # Khởi động lại script chính từ đầu
    try:
        subprocess.Popen([python, script])
    except Exception as e:
        print(f"Khởi động lại không thành công: {e}")
    finally:
        time.sleep(10)  # Đợi một chút để đảm bảo instance cũ đã ngừng hoàn toàn
        sys.exit()


import os
import sys

@bot.message_handler(commands=['rs'])
def restart_bot(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.from_user.id == ADMIN_ID:  # Chỉ admin mới được reset
        bot.reply_to(message, "Đang reset bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        bot.reply_to(message, "Bạn không có quyền reset bot.")


@bot.message_handler(commands=['tv'])
def tieng_viet(message):
    chat_id = message.chat.id
    message_id = message.message_id
    auto_react_to_command(message)  # Tự động phản hồi cảm xúc với lệnh

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🇻🇳 Tiếng Việt (Beta)", url='https://t.me/setlanguage/abcxyz'),  # Nếu có mã Beta
        types.InlineKeyboardButton("🇻🇳 Tiếng Việt (Chính thức)", url='https://t.me/setlanguage/vietnamese'),
        types.InlineKeyboardButton("🇺🇸 English", url='https://t.me/setlanguage/en'),
        types.InlineKeyboardButton("🇪🇸 Español", url='https://t.me/setlanguage/es'),
        types.InlineKeyboardButton("🇫🇷 Français", url='https://t.me/setlanguage/fr'),
        types.InlineKeyboardButton("🇷🇺 Русский", url='https://t.me/setlanguage/ru'),
        types.InlineKeyboardButton("🇨🇳 中文", url='https://t.me/setlanguage/zh-hans-raw'),
        types.InlineKeyboardButton("🇰🇷 한국어", url='https://t.me/setlanguage/ko'),
        types.InlineKeyboardButton("🇯🇵 日本語", url='https://t.me/setlanguage/ja'),
    ]


    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        '🌐 Chọn một ngôn ngữ bạn muốn sử dụng cho Telegram:',
        reply_markup=keyboard,
        parse_mode='HTML'
    )

    # Xóa tin nhắn gốc của người dùng
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        bot.send_message(chat_id,
                         f"⚠️ Không thể xóa tin nhắn: <code>{e}</code>",
                         parse_mode='HTML')



@bot.message_handler(commands=['del', 'deluser'])
def delete_user(message):
    admin_id = message.from_user.id
    auto_react_to_command(message)  # <- Thêm dòng này
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Đòi Đòi ???')
        return

    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG HOẶC UID')
        return

    user_id = int(command_parts[1])
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    if len(command_parts) == 2:
        # Xóa hoàn toàn người dùng khỏi danh sách
        if user_id in allowed_users:
            allowed_users.remove(user_id)
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id, ))
            bot.reply_to(
                message,
                f'NGƯỜI DÙNG CÓ ID {user_id} ĐÃ BỊ XÓA KHỎI DANH SÁCH.')
        else:
            bot.reply_to(message,
                         f'ID {user_id} KHÔNG TỒN TẠI TRONG DANH SÁCH.')
    elif len(command_parts) == 3:
        # Xóa thời gian VIP cụ thể
        try:
            time_to_remove = int(command_parts[2])
            cursor.execute(
                "SELECT expiration_time FROM users WHERE user_id = ?",
                (user_id, ))
            row = cursor.fetchone()
            if row:
                current_expiration = datetime.fromisoformat(row[0])
                new_expiration = current_expiration - timedelta(
                    days=time_to_remove)
                if new_expiration < datetime.now():
                    allowed_users.remove(user_id)
                    cursor.execute("DELETE FROM users WHERE user_id = ?",
                                   (user_id, ))
                    bot.reply_to(
                        message,
                        f'THỜI GIAN VIP CỦA ID {user_id} ĐÃ BỊ XÓA. NGƯỜI DÙNG ĐÃ BỊ LOẠI KHỎI DANH SÁCH.'
                    )
                else:
                    cursor.execute(
                        "UPDATE users SET expiration_time = ? WHERE user_id = ?",
                        (new_expiration.isoformat(), user_id))
                    bot.reply_to(
                        message,
                        f'THỜI GIAN VIP CỦA ID {user_id} ĐÃ BỊ GIẢM {time_to_remove} NGÀY.'
                    )
            else:
                bot.reply_to(message,
                             f'KHÔNG TÌM THẤY NGƯỜI DÙNG CÓ ID {user_id}.')
        except ValueError:
            bot.reply_to(
                message,
                'THỜI GIAN XÓA KHÔNG HỢP LỆ. VUI LÒNG NHẬP SỐ NGÀY HỢP LỆ.')

    connection.commit()
    connection.close()


@bot.message_handler(commands=['muaplan'])
def muaplan(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("🔥 Buy Vip",
                                            url='https://t.me/nmdc210')
    keyboard.add(url_button)

    bot.reply_to(
        message, "📑 <b>Mua Plan VIP</b>\n"
        "<blockquote>• 35.000 VND / 30 Ngày (Bank)\n• 40.000 VND / 30 Ngày (Card)\n• 150.000 VND / Vĩnh Viễn</blockquote>\n"
        "Liên hệ admin qua lệnh /admin để mua VIP!",
        parse_mode="HTML",
        reply_markup=keyboard)


@bot.message_handler(commands=['cachdung'])
def hdsd(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    bot.reply_to(message, f"""📑<b>HƯỚNG DẪN SỬ DỤNG</b>\n
<blockquote>┏━━━━━━━━━━━━━━━━━━━┓\n
┣➤ Để Sử Dụng Free Dùng Lệnh\n
┣➤ /sms 0123456789 5\n 
┣➤ /spam 0123456789 5\n
┣➤ 0123456789 là số muốn spam\n
┣➤ còn số 5 là số Lần spam\n
┗━━━━━━━━━━━━━━━━━━━➤\n
┏━━━━━━━━━━━━━━━━━━━┓\n
┣➤ Để Sử Dụng Vip Dùng Lệnh\n 
┣➤ /spamvip 0123456789 1000\n 
┣➤ 0123456789 là số muốn spam\n 
┣➤ còn số 1000 là số Lần spam\n 
┗━━━━━━━━━━━━━━━━━━━➤\n
┏━━━━━━━━━━━━━━━━━━━━┓\n
┣➤ Thông Tin Admin\n
┣➤ Telegram : @nmdc210\n
┗━━━━━━━━━━━━━━━━━━━➤ </blockquote>\n""",
                     parse_mode="HTML")


@bot.message_handler(commands=['muavip'])
def muavip_info(message):
    # Lấy ID người gõ lệnh
    user_id = message.from_user.id
    
    # Nội dung văn bản cần gửi cùng với ảnh
    mua_vip_text = f'''
<blockquote>
<b>Thông Tin Thanh Toán</b>
├ Ngân Hàng : Zalo Pay
├ STK : 0965934183
├ Chủ TK : Nguyen Minh Duc
├ Nội Dung : <code>muavip_{user_id}</code>
├ Số Tiền : 35.000 VND
├ Gửi bill cho @nmdc210 để được duyệt
├ LƯU Ý : PHẢI CÓ NỘI DUNG CHUYỂN KHOẢN
└ 💬 Liên Hệ : @nmdc210
</blockquote>
'''

    # Gửi ảnh kèm caption
    bot.send_photo(
        chat_id=message.chat.id,
        photo='https://sf-static.upanhlaylink.com/img/image_20251123f1cdf508b18ae97752dbf30b9624315d.jpg',
        caption=mua_vip_text,
        parse_mode='HTML'
    )
    
    
    
# Hàm gọi API reghotmail.php
import requests


# Hàm gọi API Hotmail
def create_hotmail():
    url = "https://keyherlyswar.x10.mx/Apidocs/reghotmail.php"
    try:
        response = requests.get(url, timeout=15)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Hàm lấy email & password từ JSON API (tự động dò key)
def extract_credentials(data):
    email_keys = ["email", "Email", "mail"]
    pass_keys = ["pass", "password", "Password"]

    # Nếu API trả data nested
    if isinstance(data, dict):
        # thử dò trong các key
        for key in email_keys:
            if key in data:
                email = data[key]
                break
        else:
            # dò trong data nested
            email = None
            for v in data.values():
                if isinstance(v, dict):
                    for key in email_keys:
                        if key in v:
                            email = v[key]
                            break
        for key in pass_keys:
            if key in data:
                password = data[key]
                break
        else:
            password = None
            for v in data.values():
                if isinstance(v, dict):
                    for key in pass_keys:
                        if key in v:
                            password = v[key]
                            break
    else:
        email = None
        password = None

    return email or "Không lấy được", password or "Không lấy được"

# Lệnh /reg
@bot.message_handler(commands=['reg'])
def hotmail(message):
    user_id = message.from_user.id  # Lấy user_id để check key

    # Kiểm tra key nếu đang yêu cầu
    if REQUIRE_KEY:
        ok, info = check_user_key(user_id)
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    msg = bot.send_message(message.chat.id, "⏳ Vui lòng chờ, bot đang tạo tài khoản Hotmail...")
    data = create_hotmail()

    if "error" in data:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                              text=f"❌ Lỗi: {data['error']}")
        return

    email, password = extract_credentials(data)

    result_text = (
        "✅ Tài khoản Hotmail đã tạo thành công!\n\n"
        f"📧 Email: `{email}`\n"
        f"🔑 Mật khẩu: `{password}`\n\n"
        "Admin @nmdc210"
    )

    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                          text=result_text, parse_mode="Markdown")



        
import yt_dlp
# Lệnh /ytinfo <link>
@bot.message_handler(commands=['ytb'])
def get_yt_info(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        # Lấy link từ tin nhắn
        text_split = message.text.split()
        if len(text_split) < 2:
            bot.reply_to(message, "⚠️ Vui lòng nhập link YouTube! Ví dụ:\n/ytb https://youtu.be/dQw4w9WgXcQ")
            return

        url = text_split[1]

        # Sử dụng yt_dlp để lấy thông tin video
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Lấy các thông tin cần thiết
        title = info.get("title", "Không rõ")
        uploader = info.get("uploader", "Không rõ")
        duration = info.get("duration", 0)
        view_count = info.get("view_count", 0)
        like_count = info.get("like_count", "Không rõ")
        upload_date = info.get("upload_date", "Không rõ")
        thumbnail = info.get("thumbnail", "")

        # Chuyển định dạng ngày từ YYYYMMDD sang DD/MM/YYYY
        if upload_date and len(upload_date) == 8:
            upload_date = f"{upload_date[6:]}/{upload_date[4:6]}/{upload_date[:4]}"

        # Gửi thông tin video
        caption = f"""
🎬 <b>Tiêu đề:</b> {title}
📺 <b>Kênh:</b> {uploader}
⏳ <b>Thời lượng:</b> {duration} giây
👀 <b>Lượt xem:</b> {view_count}
👍 <b>Lượt thích:</b> {like_count}
📅 <b>Ngày đăng:</b> {upload_date}
🔗 <a href="{url}">Xem video</a>
"""
        if thumbnail:
            bot.send_photo(message.chat.id, thumbnail, caption=caption, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, caption, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Lỗi khi lấy thông tin video !!!")


def anv(city):
    API_KEY = '1dcdf9b01ee855ab4b7760d43a10f854'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    tna = requests.get(base_url)
    nan = tna.json()

    if nan['cod'] == 200:
        weather_info = nan['weather'][0]['description']
        icon = nan['weather'][0]['main']
        temp_info = nan['main']['temp']
        feels_like = nan['main']['feels_like']
        temp_min = nan['main']['temp_min']
        temp_max = nan['main']['temp_max']
        city = nan['name']
        lat = nan['coord']['lat']
        lon = nan['coord']['lon']
        country = nan['sys']['country']
        all = nan['clouds']['all']
        humidity_info = nan['main']['humidity']
        wind_speed_info = nan['wind']['speed']
        feels_like_info = nan['main']['feels_like']
        gg = f"(https://www.google.com/maps/place/{nan['coord']['lat']},{nan['coord']['lon']})"
        return f'╭─────⭓Thời Tiết\n│🌍 City: {city}\n│🔗 Link map: [{city}]{gg}\n│☁️ Thời tiết: {weather_info}\n│🌡 Nhiệt độ: {temp_info}°C\n│🌡️ Nhiệt độ cảm nhận: {feels_like}°C\n│🌡️ Nhiệt độ tối đa: {temp_max}°C\n│🌡️ Nhiệt độ tối thiểu: {temp_min}°C\n│📡 Tình trạng thời tiết: {icon}\n│🫧 Độ ẩm: {humidity_info}%\n│☁️ Mức độ mây: {all}%\n│🌬️ Tốc độ gió: {wind_speed_info} m/s\n│🌐 Quốc gia: {country}.\n╰─────────────⭓'
    else:
        return 'Lệnh: thoitiet <tên thành phố>'

@bot.message_handler(commands=['thoitiet'])
def weather(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(message.text.split()) == 0:
        bot.reply_to(message, 'Nhập đúng định dạng:\n/thoitiet Hà Nội')
        return
    city = message.text.split()[1:]
    city = ' '.join(city)
    annn = anv(city)
    bot.reply_to(message, f'{annn}', parse_mode='Markdown')


is_bot_active = True

import urllib3

# Tắt cảnh báo SSL không xác thực
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@bot.message_handler(commands=['nglink', 'ngl'])
def handle_nglink(message):
    user_id = message.from_user.id
    try:
        args = message.text.split(maxsplit=3)
        if len(args) < 4:
            bot.reply_to(message, "<b>⚠️ Vui Lòng Nhập Đúng Cú Pháp</b> \n\n"
                                  "Ví dụ: \n<code>/nglink username số_lượng câu_hỏi</code>\nVD:/nglink concacc 1000 con cặc", parse_mode="HTML")
            return

        username = args[1]
        try:
            sl = int(args[2])
            if sl <= 0:
                raise ValueError
        except ValueError:
            bot.reply_to(message, "⚠️ Số Lượng Phải Là Số Nguyên Dương!")
            return

        question = args[3]
        waiting_message = bot.reply_to(message, "🐳 Đang gửi...")

        spam_ngl = f"""
╔══════════════════════
║ 🚀 SPAM NGLINK
║ •  Người Dùng : <code>{username}</code>
║ •  Nội Dung : <code>{question}</code>
║ •  Số Lượng : <code>{sl}</code>
╚══════════════════════
Muốn stop dùng /stopngl
"""
        bot.delete_message(message.chat.id, waiting_message.message_id)
        bot.reply_to(message, spam_ngl, parse_mode="HTML")

        # Gọi send_questions bằng Thread để không block bot
        thread = threading.Thread(target=send_questions, args=(user_id, username, question, sl))
        thread.start()

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi: {e}")


@bot.message_handler(commands=['stopngl'])
def stop_spam(message):
    user_id = message.from_user.id
    if active_spams.get(user_id):
        active_spamsngl[user_id] = False
        bot.reply_to(message, "🛑 Đang dừng spam... vui lòng đợi 1 chút.")
    else:
        bot.reply_to(message, "⚠️ Bạn không có spam nào đang chạy.")


import asyncio
import edge_tts
import os


@bot.message_handler(commands=['voice'])
def text_to_speech(message):
    args = message.text.split(maxsplit=1)
    auto_react_to_command(message)  # <- Thêm dòng này

    if len(args) < 2:
        bot.reply_to(message, "Sai cú pháp! Dùng:\n/voice văn bản", parse_mode="Markdown")
        return

    text = args[1]
    file_path = "output.mp3"
    voice = "vi-VN-NamMinhNeural"  # Giọng nam tiếng Việt

    async def generate_voice():
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(file_path)

            with open(file_path, "rb") as audio:
                bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id)

            os.remove(file_path)
        except Exception as e:
            bot.reply_to(message, f"Đã xảy ra lỗi: {str(e)}")

    asyncio.run(generate_voice())


from urllib.parse import urlparse
import zipfile


def sanitize_filename(name):
    return re.sub(r'\W+', '_', name)[:50]

@bot.message_handler(commands=['code'])
def handle_code(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            bot.reply_to(message, "Vui lòng nhập đúng lệnh: /code <url>\nVD: /code https://vlxx.com.mssg.me/")
            return

        url = args[1].strip()
        if not url.startswith("http"):
            url = "http://" + url

        parsed_url = urlparse(url)
        domain = sanitize_filename(parsed_url.netloc)
        zip_filename = f"{domain}_source.zip"

        # Lấy mã HTML
        response = requests.get(url, timeout=15)
        response.encoding = response.apparent_encoding
        html = response.text

        # Phân tích HEAD và BODY
        soup = BeautifulSoup(html, "html.parser")
        head = soup.head.prettify() if soup.head else "Không có thẻ <head>"
        body = soup.body.prettify() if soup.body else "Không có thẻ <body>"

        # Tạo file tạm
        with open("full.html", "w", encoding="utf-8") as f:
            f.write(html)
        with open("head.html", "w", encoding="utf-8") as f:
            f.write(head)
        with open("body.html", "w", encoding="utf-8") as f:
            f.write(body)

        # Nén file ZIP
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write("full.html")
            zipf.write("head.html")
            zipf.write("body.html")

        # Gửi file ZIP
        with open(zip_filename, "rb") as f:
            bot.send_document(message.chat.id, f, caption=f"Toàn bộ mã nguồn từ {url} của bạn yêu cầu.", reply_to_message_id=message.message_id)

        # Xóa file tạm
        for file in ["full.html", "head.html", "body.html", zip_filename]:
            if os.path.exists(file):
                os.remove(file)

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"❌ Không thể truy cập URL: {e}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi: {e}")

from deep_translator import GoogleTranslator
@bot.message_handler(commands=['dich'])
def translate_command(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Vui lòng nhập từ hoặc câu cần dịch.\nVí dụ: /dich concac lap trinh nhu cac")
        return

    text_to_translate = args[1]
    try:
        translated = GoogleTranslator(source="auto", target="vi").translate(text_to_translate)
        bot.reply_to(message, f"Dịch: {translated}")
    except Exception as e:
        bot.reply_to(message, f"Lỗi dịch: {str(e)}")


# File chứa danh sách link (mỗi dòng 1 link .mp4)
TIKTOK_FILE = "tiktok_links.txt"

def get_all_links_from_file():
    """
    Đọc tất cả link từ TIKTOK_FILE, trả về list (loại bỏ dòng rỗng & comment).
    """
    links = []
    try:
        with open(TIKTOK_FILE, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                # Bỏ qua dòng bắt đầu bằng # (comment)
                if s.startswith("#"):
                    continue
                links.append(s)
    except FileNotFoundError:
        return []
    except Exception:
        # nếu có lỗi đọc file, trả về rỗng
        return []
    return links

def get_random_tiktok_link():
    """
    Lấy 1 link ngẫu nhiên từ file, trả về None nếu file rỗng hoặc không tồn tại.
    """
    links = get_all_links_from_file()
    if not links:
        return None
    return random.choice(links)

# Handler lệnh /videogai
@bot.message_handler(commands=['videogai'])
def send_random_video(message):
    try:
        auto_react_to_command(message)
    except Exception:
        pass

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Nếu hệ thống bắt buộc key, kiểm tra trước (nếu bạn dùng cơ chế key)
    try:
        if REQUIRE_KEY:
            ok, info = check_user_key(user_id)
            if not ok:
                return bot.reply_to(
                    message,
                    "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n👉 Lấy key bằng lệnh /getkey và nhập /key <mã-key>.",
                    parse_mode="HTML"
                )
    except Exception:
        # nếu check key lỗi thì vẫn tiếp tục (tuỳ bạn)
        pass

    link = get_random_tiktok_link()
    if not link:
        return bot.reply_to(chat_id, "❌ Không tìm thấy link trong file hoặc file trống (tiktok_links.txt).")

    # Gửi video bằng URL nếu Telegram hỗ trợ URL trực tiếp
    try:
        # dùng send_video với video=url
        bot.send_chat_action(chat_id, 'upload_video')
        bot.send_video(chat_id, video=link, caption="🎬 Video Gái nè thằng dâm.", reply_to_message_id=message.message_id)
    except Exception as e:
        # Nếu gửi bằng URL thất bại (server từ chối), fallback: tải về rồi gửi file
        try:
            bot.send_message(chat_id, "⚠️ Mày Không Có Số Xem Gái.")
            r = requests.get(link, stream=True, timeout=20)
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                for chunk in r.iter_content(chunk_size=1024*64):
                    if chunk:
                        tmp.write(chunk)
                tmp_path = tmp.name
            # gửi file từ tmp_path
            with open(tmp_path, 'rb') as f:
                bot.send_video(chat_id, f, caption="🎬 Video ngẫu nhiên", reply_to_message_id=message.message_id)
        except Exception as e2:
            bot.reply_to(chat_id, f"❌ Không thể gửi video: {e2}")
        finally:
            # xoá file tạm nếu có
            try:
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass   

import time
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import my_pb2
import output_pb2
import schedule
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'


TAOANH_URL = "https://seaart-ai.apis-bj-devs.workers.dev/?Prompt={text}"
@bot.message_handler(commands=['taoanh'])
def tao_anh(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    username = message.from_user.username
    try:
        text = message.text.replace("/taoanh", "").strip()
        if not text:
            bot.reply_to(message, "Vui lòng nhập mô tả ảnh.\n Ví dụ: /taoanh nmdc210")
            return

        # Gửi tin nhắn thông báo
        status_msg = bot.reply_to(message, "Đang tạo ảnh, vui lòng đợi...")

        response = requests.get(TAOANH_URL.format(text=text)).json()
        if response["status"] == "success":
            images = response["result"]
            for img in images:
                bot.send_photo(message.chat.id, img["url"], caption=f"📸🏞ẢNH BẠN YÊU CẦU @{username}", reply_to_message_id=message.message_id)

        else:
            bot.reply_to(message, "Không thể tạo ảnh, vui lòng thử lại sau!")

        # Xóa tin nhắn "Đang tạo ảnh..."
        time.sleep(2)  # Chờ 2 giây để đảm bảo ảnh đã gửi xong
        bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"Lỗi: {str(e)}")

import requests
from telebot.types import InputFile

soundcloud_data = {}
PLATFORM = "soundcloud"
API_BASE = "https://api-v2.soundcloud.com"
CONFIG_PATH = "config.json"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]
ACCEPT_LANGUAGES = ["en-US,en;q=0.9", "fr-FR,fr;q=0.9", "es-ES,es;q=0.9", "de-DE,de;q=0.9", "zh-CN,zh;q=0.9"]

def get_random_element(array):
    return random.choice(array)

def get_headers():
    return {
        "User-Agent": get_random_element(USER_AGENTS),
        "Accept-Language": get_random_element(ACCEPT_LANGUAGES),
        "Referer": "https://soundcloud.com/",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

def get_client_id():
    try:
        import os
        config = {}
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            if config.get('client_id'):
                return config['client_id']

        response = requests.get("https://soundcloud.com/", headers=get_headers())
        response.raise_for_status()
        script_tags = re.findall(r'<script crossorigin src="([^"]+)"', response.text)
        script_urls = [url for url in script_tags if url.startswith("https")]

        if not script_urls:
            raise ValueError("No script URLs found")

        script_response = requests.get(script_urls[-1], headers=get_headers())
        script_response.raise_for_status()
        client_id_match = re.search(r',client_id:"([^"]+)"', script_response.text)
        if not client_id_match:
            raise ValueError("Client ID not found in script")

        client_id = client_id_match.group(1)

        config['client_id'] = client_id
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

        return client_id
    except Exception as e:
        print(f"Error fetching client ID: {e}")
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            return config.get('client_id', 'MHDG7vIKasWstY0FaB07rK5WUoUjjCDC')
        return 'MHDG7vIKasWstY0FaB07rK5WUoUjjCDC'

def get_music_info(question, limit=10):
    try:
        client_id = get_client_id()
        response = requests.get(
            f"{API_BASE}/search/tracks",
            params={
                "q": question,
                "variant_ids": "",
                "facet": "genre",
                "client_id": client_id,
                "limit": limit,
                "offset": 0,
                "linked_partitioning": 1,
                "app_locale": "en",
            },
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching music info: {e}")
        return None

def get_music_stream_url(track):
    try:
        client_id = get_client_id()
        api_url = f"{API_BASE}/resolve?url={track['permalink_url']}&client_id={client_id}"
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        data = response.json()

        progressive_url = next(
            (t['url'] for t in data.get('media', {}).get('transcodings', []) if t['format']['protocol'] == 'progressive'),
            None
        )
        if not progressive_url:
            raise ValueError("No progressive transcoding URL found")

        stream_response = requests.get(
            f"{progressive_url}?client_id={client_id}&track_authorization={data.get('track_authorization', '')}",
            headers=get_headers()
        )
        stream_response.raise_for_status()
        return stream_response.json()['url']
    except Exception as e:
        print(f"Error getting music stream URL: {e}")
        return None

@bot.message_handler(commands=['scl'])
def soundcloud(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "🚫 Vui lòng nhập tên bài hát muốn tìm kiếm.\nVí dụ: /scl Tên bài hát", parse_mode='HTML')
        return
    keyword = args[1].strip()
    music_info = get_music_info(keyword)
    if not music_info or not music_info.get('collection') or len(music_info['collection']) == 0:
        bot.reply_to(message, "🚫 Không tìm thấy bài hát nào khớp với từ khóa.", parse_mode='HTML')
        return
    tracks = [track for track in music_info['collection'] if track.get('artwork_url')]
    if not tracks:
        bot.reply_to(message, "🚫 Không tìm thấy bài hát nào có hình ảnh.", parse_mode='HTML')
        return
    response_text = "<b>🎵 Kết quả tìm kiếm trên SoundCloud</b>\n\n"
    for i, track in enumerate(tracks):
        response_text += f"<b>{i + 1}. {track['title']}</b>\n"
        response_text += f"👤 Nghệ sĩ: {track['user']['username']}\n"
        response_text += f"📊 Lượt nghe: {track['playback_count']:,} | Thích: {track['likes_count']:,}\n"
        response_text += f"🆔 ID: {track['id']}\n\n"
    response_text += "<b>💡 Trả lời tin nhắn này bằng số từ 1-10 để chọn bài hát!</b>"
    sent = bot.reply_to(message, response_text, parse_mode='HTML')
    soundcloud_data[sent.message_id] = {
        "user_id": message.from_user.id,
        "tracks": tracks
    }

@bot.message_handler(func=lambda msg: msg.reply_to_message and msg.reply_to_message.message_id in soundcloud_data)
def handle_soundcloud_selection(msg):
    reply_id = msg.reply_to_message.message_id
    if reply_id not in soundcloud_data:
        return
    user_id = msg.from_user.id
    data = soundcloud_data[reply_id]
    if user_id != data['user_id']:
        return
    text = msg.text.strip().lower()
    try:
        index = int(text.split()[0]) - 1
        if index < 0 or index >= len(data["tracks"]):
            bot.reply_to(msg, "🚫 Số không hợp lệ. Hãy nhập số từ 1-10.", parse_mode='HTML')
            return
    except (ValueError, IndexError):
        bot.reply_to(msg, "🚫 Vui lòng nhập số từ 1-10.", parse_mode='HTML')
        return
    track = data["tracks"][index]
    bot.reply_to(msg, f"🧭 Đang tải: {track['title']}", parse_mode='HTML')
    audio_url = get_music_stream_url(track)
    thumbnail_url = track.get('artwork_url', '').replace("-large", "-t500x500")
    if not audio_url or not thumbnail_url:
        bot.reply_to(msg, "🚫 Không tìm thấy nguồn audio hoặc thumbnail.", parse_mode='HTML')
        return
    caption = f"<b>🎵 {track['title']}</b>\n"
    caption += f"👤 Nghệ sĩ: {track['user']['username']}\n"
    caption += f"📊 Lượt nghe: {track['playback_count']:,} | Thích: {track['likes_count']:,}\n"
    caption += f"🎧 Nguồn: SoundCloud\n"
    caption += f"🎉 Chúc bạn thưởng thức âm nhạc vui vẻ!"
    try:
        bot.delete_message(msg.chat.id, reply_id)
    except:
        pass
    bot.send_photo(msg.chat.id, thumbnail_url, caption=caption, parse_mode='HTML')
    bot.send_audio(msg.chat.id, audio_url, title=track['title'], performer=track['user']['username'])
    del soundcloud_data[reply_id]


# --- Hàm load danh sách bảo trì từ file ---
def load_maintenance():
    import baotri
    importlib.reload(baotri)  # reload file để cập nhật khi có thay đổi
    return set(baotri.maintenance_commands)

# --- Hàm lưu danh sách bảo trì ra file ---
def save_maintenance(commands):
    with open("baotri.py", "w", encoding="utf-8") as f:
        f.write("# Danh sách lệnh đang bảo trì\n")
        f.write("maintenance_commands = [\n")
        for cmd in commands:
            f.write(f'    "{cmd}",\n')
        f.write("]\n")

# --- Lệnh /baotri <lenh> (bật bảo trì) ---
@bot.message_handler(commands=['baotri'])
def handle_baotri(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ Bạn không có quyền dùng lệnh này.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Dùng: /baotri <lenh>")
        return

    cmd = args[1].lower()
    maintenance = load_maintenance()
    if cmd in maintenance:
        bot.reply_to(message, f"⚠️ Lệnh `{cmd}` đã trong bảo trì rồi.")
    else:
        maintenance.add(cmd)
        save_maintenance(maintenance)
        bot.reply_to(message, f"✅ Đã thêm lệnh `{cmd}` vào bảo trì.")

# --- Lệnh /hoatdong <lenh> (gỡ bảo trì) ---
@bot.message_handler(commands=['hoatdong'])
def handle_hoatdong(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ Bạn không có quyền dùng lệnh này.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Dùng: /hoatdong <lenh>")
        return

    cmd = args[1].lower()
    maintenance = load_maintenance()
    if cmd not in maintenance:
        bot.reply_to(message, f"⚠️ Lệnh `{cmd}` không nằm trong bảo trì.")
    else:
        maintenance.remove(cmd)
        save_maintenance(maintenance)
        bot.reply_to(message, f"✅ Đã gỡ bảo trì lệnh `{cmd}`.")

# --- Lệnh /listbaotri ---
@bot.message_handler(commands=['listbaotri'])
def handle_list_baotri(message):
    maintenance = load_maintenance()
    if not maintenance:
        bot.reply_to(message, "✅ Hiện không có lệnh nào đang bảo trì.")
    else:
        cmds = "\n".join([f"• {cmd}" for cmd in maintenance])
        bot.reply_to(message, f"⚠️ Danh sách lệnh đang bảo trì:\n{cmds}")

# --- Check lệnh có đang bảo trì không ---
def is_under_maintenance(cmd):
    return cmd in load_maintenance()

USERS_FILE = "users.txt"

# --- Lưu user vào file ---
def save_user(user_id):
    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("")
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if user_id not in users:
        with open(USERS_FILE, "a") as f:
            f.write(user_id + "\n")

# --- Lấy danh sách user từ file ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return f.read().splitlines()

# --- Khi bất kỳ ai nhắn bot thì lưu user ---
@bot.message_handler(func=lambda message: True)
def save_all_users(message):
    save_user(message.from_user.id)

# --- Lệnh /thongbao <văn bản> ---
@bot.message_handler(commands=['thongbao'])
def handle_broadcast(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ Bạn không có quyền dùng lệnh này.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Dùng: /thongbao <nội dung>")
        return

    content = args[1]
    users = load_users()

    success = 0
    fail = 0
    for uid in users:
        try:
            bot.send_message(uid, f"📢 Thông báo từ Admin:\n\n{content}")
            success += 1
        except:
            fail += 1

    bot.reply_to(message, f"✅ Đã gửi thông báo đến {success} người dùng.\n❌ Lỗi: {fail}.")


# Tạo thư mục lưu trữ nếu chưa có
import json, os, random
from telebot.types import ReplyKeyboardMarkup

# --- Cấu hình ---
users_file = "users.json"
login_file = "login.json"
code_file = "codes.json"
register_temp = {}
admin_id = [6836012166]  # Thay bằng Telegram ID admin

# --- Hàm tiện ích ---
def load_json(file):
    if not os.path.exists(file): open(file, "w").write("{}")
    with open(file) as f: return json.load(f)

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

# --- MENU ---





import random
import logging
emoji_list = [
    '👍',  # Like
    '👎',  # Dislike
    '❤️',  # Heart
    '🔥',  # Fire
    '👏',  # Clapping
    '😁',  # Grinning
    '😢',  # Crying
    '😮',  # Surprised
    '😡',  # Angry
    '🤯',  # Mind blown
    '🥳',  # Party
    '🤔',  # Thinking
    '🤡',  # Clown
    '💩',  # Poop
    '🙈',  # See no evil
    '😎',  # Cool
    '💯',  # 100
    '🥴',  # Dizzy
    '😆',  # Laughing hard
    '😐',  # Neutral
    '🤮',  # Vomit
    '🫡',  # Salute (mới hơn)
    '🙃',  # Upside down
    '💋',  # Kiss
    '😈',  # Smiling devil
    '👀',  # Eyes
    '🤗',  # Hug
    '☠️',  # Skull
    '🫶',  # Heart hands
]

# Trạng thái auto reaction cho từng nhóm
react_status = {}

# Kiểm tra admin
def is_user_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception as e:
        print(f"Lỗi kiểm tra admin: {e}")
        return False

# Hàm thả cảm xúc thật
def tha_camxuc(chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'reaction': json.dumps([{'type': 'emoji', 'emoji': emoji}])
    }
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Lỗi khi gọi API thả cảm xúc: {e}")
        return None

# Hàm gọi auto thả cảm xúc
def auto_react_to_command(message):
    chat_id = message.chat.id
    message_id = message.message_id

    if message.from_user.id == bot.get_me().id:
        return

    if not react_status.get(chat_id, True):
        return

    random_emoji = random.choice(emoji_list)
    print(f"Thả cảm xúc {random_emoji} cho lệnh {message.text}")

    result = tha_camxuc(chat_id, message_id, random_emoji)
    if not result or not result.get('ok'):
        print(f"Lỗi thả cảm xúc: {result.get('description') if result else 'Không rõ lỗi'}")
        if random_emoji != "🎉":
            tha_camxuc(chat_id, message_id, "🎉")

# Lệnh /react để bật/tắt auto
@bot.message_handler(commands=['react'], chat_types=['group', 'supergroup'])
def toggle_react(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Chỉ admin mới được dùng lệnh này!")
        return

    current_state = react_status.get(chat_id, True)
    state_text = "BẬT" if current_state else "TẮT"

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Bật tự động", callback_data="react_on"),
        InlineKeyboardButton("Tắt tự động", callback_data="react_off")
    )
    keyboard.row(InlineKeyboardButton("Đóng", callback_data="react_close"))

    bot.send_message(chat_id, f"Chế độ tự động thả cảm xúc hiện đang {state_text}. Chọn tùy chọn:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('react_'))
def handle_react_callback(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data

    if not is_user_admin(chat_id, user_id):
        bot.answer_callback_query(call.id, "Chỉ admin mới được dùng tính năng này!", show_alert=True)
        return

    if data == "react_on":
        react_status[chat_id] = True
        new_text = "✅ Đã bật chế độ tự động thả cảm xúc!"
    elif data == "react_off":
        react_status[chat_id] = False
        new_text = "❌ Đã tắt chế độ tự động thả cảm xúc!"
    elif data == "react_close":
        try:
            bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f"Lỗi xóa tin nhắn: {e}")
        return

    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Đóng", callback_data="react_close"))

    try:
        bot.edit_message_text(new_text, chat_id, message_id, reply_markup=keyboard)
    except Exception as e:
        print(f"Lỗi khi sửa tin nhắn: {e}")

    bot.answer_callback_query(call.id)

# Xử lý các tin nhắn thường (không phải lệnh)
# ❌ Không thả cảm xúc cho tin nhắn thường
@bot.message_handler(func=lambda m: m.text and not m.text.startswith("/"), chat_types=['group', 'supergroup'])
def ignore_regular_messages(message):
    pass  # Bỏ qua tin nhắn thường

# ✅ Thả cảm xúc cho tất cả các lệnh
@bot.message_handler(func=lambda m: m.text and m.text.startswith("/"), chat_types=['group', 'supergroup'])
def react_to_command(message):
    auto_react_to_command(message)

    
if __name__ == "__main__":
    bot_active = True
    bot.infinity_polling()



