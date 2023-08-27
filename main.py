import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import datetime

bot_token = '6240454459:AAFBIqeSS9zqo49dbdiZ2Fqlwk8hjqSoJ70' 
bot = telebot.TeleBot(bot_token)

allowed_group_id = -980183071

allowed_users = []
processes = []
ADMIN_ID = 5531966867

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()

def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, '🚀BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY🚀')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, '🚀VUI LÒNG NHẬP ID NGƯỜI DÙNG 🚀')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'🚀NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spam.🚀')


load_users_from_database()

@bot.message_handler(commands=['laykey'])
def laykey(message):
    bot.reply_to(message, text='🚀VUI LÒNG ĐỢI TRONG GIÂY LÁT!🚀')

    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    url_key = requests.get(f'https://link4m.co/api-shorten/v2?api=6482889a387b655919802cfa&url=https://trummailcovip.site/keytele/?key={key}').json()['shortenedUrl']
    
    text = f'''
- LINK KEY {TimeStamp()}:{url_key} 
- DÙNG LỆNH /key {{key}} ĐỂ TIẾP TỤC -
 🚀[Lưu ý :mỗi key chỉ có 1 người dùng]🚀
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, '🚀VUI LÒNG NHẬP KEY.🚀')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, '🚀KEY HỢP LỆ. BẠN ĐÃ ĐƯỢC PHÉP SỬ DỤNG LỆNH /spam.🚀\n[Lưu ý :mỗi key chỉ có 1 người dùng] ')
    else:
        bot.reply_to(message, '🚀KEY KHÔNG HỢP LỆ.🚀\n[Lưu ý :mỗi key chỉ có 1 người dùng]')

@bot.message_handler(commands=['spam'])
def lqm_sms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, text='🚀BẠN CHƯA NHẬP KEY ,VUI LÒNG NHẬP KEY ĐỂ SỬ DỤNG LỆNH NÀY!🚀')
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, '🚀VUI LÒNG NHẬP SỐ ĐIỆN THOẠI🚀 ')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, '🚀SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !🚀')
        return

    if phone_number in ['113','911','114','115','+84346452531','0949404151','0355366216','']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"Spam cái đầu buồi °đây là sdt của admin° tao ban mày luôn bây giờ")
        return

    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "120"])
    processes.append(process)
    bot.reply_to(message, f'┏━━━━━━━━━━━━━━━━━━┓\n┣➤ 🚀 Gửi Yêu Cầu Tấn Công Thành Công 🚀 \n┣➤ Bot 👾: @ClarityLuck_BOT \n┣➤ Số Tấn Công 📱: [ {phone_number} ]\n┣➤Thời gian 🕐: 120s ✅\n┗━━━━━━━━━━━━━━━━━━┛\n')

@bot.message_handler(commands=['how'])
def how_to(message):
    how_to_text = '''
━━➤ 🚀Hướng dẫn sử dụng🚀.

┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┣➤ - Sử dụng lệnh để lấy key. [/laykey]             
┣➤ - Chạy bot spam gọi điện + sms. [/spam]
┣➤ - Khi lấy key xong, sử dụng lệnh để kiểm tra. [/key]
┣➤ - Key hợp lệ mới có quyền sử dụng các lệnh trên.
┣➤ - Website của admin: gbaodz.com.
┗━━━━━━━━━━━━━━━━━━━━━━━━┛
'''
    bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['help'])
def help(message):
    help_text = '''
━━➤ 🚀Danh sách lệnh:🚀
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┣➤ - Sử dụng lệnh để lấy key. [/laykey]
┣➤ - Chạy bot spam gọi điện + sms. [/spam] 
┣➤ - Ví Dụ: /spam 0346455555 Để spam call + sms
┣➤ - Lấy key xong, sử dụng lệnh để kiểm tra. [/key]
┣➤ - Hướng dẫn sử dụng. [/how]
┣➤ - Danh sách lệnh. [/help]
┣➤ - website của admin: gbaodz.com.
┗━━━━━━━━━━━━━━━━━━━━━━━┛
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, '🚀Bạn không có quyền sử dụng lệnh này.🚀')
        return
    if user_id not in allowed_users:
        bot.reply_to(message, text='🚀Bạn không có quyền sử dụng lệnh này!🚀')
        return
    process_count = len(processes)
    bot.reply_to(message, f'🚀Số quy trình đang chạy:🚀 {process_count}.')

@bot.message_handler(commands=['cpu'])
def cpu(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, "Bạn không có quyền thực hiện lệnh này.")
        return

    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    message_text = f"🖥 Thông tin hệ thống 🖥\n\n" \
                   f"📊 CPU: {cpu_percent}%\n" \
                   f"🧠 Memory: {memory_percent}%"
    bot.reply_to(message, message_text)

def start_polling():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Threaded polling exception: {e}")
            time.sleep(5)

@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, '🚀Bạn không có quyền sử dụng lệnh này.🚀')
        return

    bot.reply_to(message, '🚀Bot sẽ được khởi động lại trong giây lát...🚀')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, '🚀Bạn không có quyền sử dụng lệnh này.🚀')
        return

    bot.reply_to(message, '🚀Bot sẽ dừng lại trong giây lát..🚀.')
    time.sleep(2)
    bot.stop_polling()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, '🚀Lệnh không hợp lệ. Vui lòng sử dụng lệnh /help để xem danh sách lệnh.🚀')

bot.polling()
