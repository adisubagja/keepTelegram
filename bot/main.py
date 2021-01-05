from bot import dbWorker
import os
import time
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))


# ------------ Program functions start ------------ #
def note_template(data):
    return f"""
<strong>Header</strong>: <i>{data[1]}</i>
<strong>Text</strong>: <i>{data[2]}</i>
<strong>Status</strong>: <i>{data[3]}</i>
<strong>Due time</strong>: <i>{data[4]}</i>
"""
# ------------ Program functions end ------------ #


# ------------ Bot functions start ------------ #
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Hello, how are you?')


@bot.message_handler(commands=['add'])
def add_note(message):
    chat_id = message.chat.id
    data = message.text.split('\n')[1:]
    timestamp = time.time()
    print(data)
    if len(data) == 3:
        conn = dbWorker.connect(os.getenv('DB_PATH'))
        note = dbWorker.get(conn.cursor(), 'id', timestamp)
        if not note:
            dbWorker.add(
                conn, conn.cursor(), [
                    chat_id, data[0], data[1], 0, data[2], timestamp])
            conn.close()
            bot.send_message(chat_id, f'Your note with the header \"{data[0]}\" has been added')
        else:
            bot.send_message(chat_id, f'Note with the header \"{data[0]}\" exists')
    else:
        bot.send_message(chat_id, 'Please, write you message correctly')
    print('Closing connection is successful')


@bot.message_handler(commands=['get'])
def get_notes(message):
    bot.reply_to(message, 'Your notes:')
    conn = dbWorker.connect(os.getenv('DB_PATH'))
    chat_id = message.chat.id
    data = dbWorker.get(conn.cursor(), 'chat_id', chat_id)
    for note in data:
        msg = note_template(note)
        bot.send_message(chat_id, msg, parse_mode='HTML')
    conn.close()
    print('Closing connection is successful')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# ------------ Bot functions end ------------ #


print("Bot started")
bot.polling(none_stop=True, interval=0)
