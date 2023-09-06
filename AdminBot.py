import UserBot
import telebot
import sqlite3
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

global values
values = []
def save_value(value):
    values.append(value)

bot = telebot.TeleBot('5126593402:AAEfXHEWX7jSzm6EbMBL54_AeJuBAMrnbhA', parse_mode=None)
bot1 = telebot.TeleBot('5182505143:AAEYBnvNTpo0x8GFF8Udf_Tx6vgV6HTm9-U', parse_mode=None)
userbot = telebot.TeleBot("5157667764:AAFt2kpWpEHrWTMOu3JnC4GgzzS6bCahsWc")


markupRemove = types.ReplyKeyboardRemove()

global adminID
adminID = [392848013, 544293144, 444390651]


@bot.message_handler(commands=['start', 'check_table', 'answer_user', 'create_topic', 'show_topics_list'])
def start(message):
    if message.from_user.id in adminID:

        if message.text == '/start':
            bot.send_message(message.chat.id, "Hello, Master", reply_markup=markupRemove)

        elif message.text == '/check_table':
            db = conn.cursor().execute("SELECT * FROM 'Default'").fetchall()
            print(db)
            table = ""
            for i in db:
                table += "'" + i[1] + "'" + " \nby user id: " + str(i[2]) + "\n\n"
            bot.send_message(message.chat.id, table)

        elif message.text == '/answer_user':
            mestemp = bot.send_message(message.chat.id, "Кому ответить? Введи id")
            bot.register_next_step_handler(mestemp, getID)

        elif message.text == '/create_topic':
            mestemp = bot.send_message(message.chat.id,
                                       "Введите название новой темы")
            bot.register_next_step_handler(mestemp, get_name_topic)

        elif message.text == '/show_topics_list':
            show_topics_list(message)

        elif message.text == '/show_topic':
            mestemp = bot.send_message(message.chat.id,
                                       "Введите номер темы\n"
                                       "Его можно узнать, вызвав команду '/show_topics_list'")
            bot.register_next_step_handler(mestemp, choose_topic)

    else:
        bot.send_message(message.chat.id, "У вас недостаточно прав")

def getID(message):
    userID = int(message.text)
    save_value(userID)
    mestemp = bot.send_message(message.chat.id, "Введите текст сообщения")
    bot.register_next_step_handler(mestemp, answer_to_user)


def answer_to_user(message):
    userID = values[-1]
    userbot.send_message(userID, message.text)


def get_name_topic(message):
    topic_name = message.text
    create_topic_table(conn.cursor(), topic_name)
    bot.send_message(message.chat.id,
                     f"Таблица для темы {topic_name} создана")

def create_topic_table(cursor, topic_name):
    parameters = f'''
        CREATE TABLE IF NOT EXISTS '{topic_name}'
        (id_msg integer PRIMARY KEY,
        txt_msg text not null,
        userid integer not null)
        '''
    conn.cursor().execute(parameters)


def show_topics_list(message):
    topics = get_all_topics(conn.cursor())
    topicsStr = ""
    count = 1
    for i in topics:
        topicsStr += (str(count) + ") " + str(i)[2:-3] + "\n\n")
        print(i[0])
        count += 1
    bot.send_message(message.chat.id, topicsStr)


def get_all_topics(cursor):
    return cursor.execute('SELECT name from sqlite_master where type="table"').fetchall()


def choose_topic(message):
    bot.send_message(message.chat.id,
                     "Функция пока недоступна")
    #if type(message.text) == int:
        #topics = get_all_topics(conn.cursor())
        #if (message.text > len(topics) or message.text < 1):
            #mestemp =
    #else:
        #mestemp = bot.send_message(message.chat.id, "Введите число")
        #bot.register_next_step_handler(mestemp, choose_topic)




conn = sqlite3.connect("user's_topics.db", check_same_thread=False)




bot.infinity_polling()