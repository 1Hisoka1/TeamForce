import telebot
import telegram
from telebot import types
import sqlite3

values = []
def save_value(value):
    values.append(value)


def make_topics_buttons(cursor):
   return cursor.execute('SELECT name from sqlite_master where type= "table"').fetchall()

def print_table(cursor, table):
    return cursor.execute(f"SELECT title_question FROM '{table}'").fetchall()


def create_table(cursor, table_name):
    parameters = f'''CREATE TABLE IF NOT EXISTS '{table_name}'(id_quest integer PRIMARY KEY, 
    title_question text not null,
        answer_question text not null);'''
    cursor.execute(parameters)


def create_admin_questions(cursor, table_name):
    parameters = f'''CREATE TABLE IF NOT EXISTS '{table_name}' (id_msg integer PRIMARY KEY, 
    txt_msg text not null, userid_msg integer not null)'''
    cursor.execute(parameters)

#botToken = "5283889178:AAEc5X8Hjn6Y953lwSY9HhIYYbg7XMS3dec"


global error_wrongAnswer
error_wrongAnswer = "Сейчас запущена друга команда\nПопробуй еще раз"

global adminID
adminID = 392848013

commands = ['/admin_help', '/start', '/create_topic']

markupStart = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Список тем")
markupStart.add(btn1)


def add_question(question, answer):
    conn.cursor().execute("INSERT INTO questions (title_question, answer_question) VALUES (?,?)", (question, answer))


def create_buttons_list(cursor, table):
    markupQList = types.ReplyKeyboardMarkup(resize_keyboard=True)
    questions_list = cursor.execute(f"SELECT title_question FROM '{table}'").fetchall()
    for i in questions_list:
        markupQList.add(types.KeyboardButton(i[0]))
    return markupQList


def show_questions(new_message):
    conn1 = sqlite3.connect('quest.db')
    topic = str(new_message.text)
    a = []
    flag = False
    if new_message.text == '/admin_help':
        save_message_for_admin(new_message)
        return

    for i in make_topics_buttons(conn1.cursor()):
        if (str(i)[2:-3]) == topic:
            flag = True

    if flag:
        markupQuestions = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markupQuestions = create_buttons_list(conn1.cursor(), topic)
        sm1 = bot.send_message(new_message.chat.id, "Выберите вопрос из списка", reply_markup=markupQuestions)
        save_value(topic)
        bot.register_next_step_handler(sm1, show_answer)

    else:
        sm = bot.send_message(new_message.chat.id, error_wrongAnswer)
        bot.register_next_step_handler(sm, show_questions)


markupEnding = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnYes = types.KeyboardButton('Да')
btnNo = types.KeyboardButton('Нет')
markupEnding.add(btnYes, btnNo)

markupRemove = types.ReplyKeyboardRemove()


def show_answer(newest_message):
    conn2 = sqlite3.connect('quest.db')

    if newest_message.text == '/admin_help':
        save_message_for_admin(newest_message)
        return

    question = str(newest_message.text)
    topic = values[-1]
    if len(values) > 100:
        values.clear()

    print(topic, question)
    answer = conn2.cursor().execute(f"SELECT answer_question FROM  '{topic}' WHERE title_question = '{question}'").fetchone()
    bot.send_message(newest_message.chat.id, answer)
    yesno = bot.send_message(newest_message.chat.id, "Остались вопросы?", reply_markup=markupEnding)
    bot.register_next_step_handler(yesno, end_bot)


def end_bot(message):
    if message.text == 'Да':
        show_topics(message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "Удачи\nЧтобы начать заново, Введите '/start'", reply_markup=markupRemove)
    else:
        bot.send_message(message.chat.id, "Бот вас не понял, но на всякий случай отключился..."
                                          "\nДля запуска бота, пиши '/start'", reply_markup=markupRemove)


def saveMsgInDB(message):
    create_admin_questions(connTopics.cursor(), "Default")

    userid = message.from_user.id
    msgtext = message.text

    parameters = f'''
    INSERT INTO
        'Default' (txt_msg, userid_msg)
    VALUES
        ('{msgtext}', {userid})
    '''
    connTopics.cursor().execute(parameters)
    connTopics.commit()

    print(msgtext, userid)

    bot.send_message(message.chat.id, "Сообщение доставлено администратору\n"
                                      "Ожидайте ответа")


def show_topics(message):
    sm = bot.send_message(
        message.chat.id, "Список тем:",
        reply_markup=markupTopicsList)
    bot.register_next_step_handler(sm, show_questions)


def save_message_for_admin(message):

    m1 = bot.send_message(message.chat.id,
                           "Введите сообщение, которое нужно отправить администратору",
                           reply_markup=markupRemove)
    bot.register_next_step_handler(m1, saveMsgInDB)


if __name__ == "__main__":

    global botToken
    botToken = "5157667764:AAFt2kpWpEHrWTMOu3JnC4GgzzS6bCahsWc"
    bot = telebot.TeleBot(botToken)

    print(123)
    conn = sqlite3.connect('quest.db')
    create_table(conn.cursor(), "Авторизация")
    create_table(conn.cursor(), "Проблемы со здоровьем")
    create_table(conn.cursor(), "Ушла жена")

    connTopics = sqlite3.connect("user's_topics.db", check_same_thread=False)

    markupTopicsList = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in make_topics_buttons(conn.cursor()):
        markupTopicsList.add(types.KeyboardButton(i[0]))

    @bot.message_handler(commands=['start', 'admin_help'])
    def do_commands(message):
        if message.text == '/start':
            bot.send_message(message.chat.id, "Добро пожаловать в нашего бота, "
                             "{0.first_name}!\nВыберите тему вопроса".format(message.from_user))
            show_topics(message)

        elif message.text == '/admin_help':
            save_message_for_admin(message)


    bot.infinity_polling()
    bot.stop_bot()
