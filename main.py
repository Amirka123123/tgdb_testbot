import telebot
import sqlite3

TOKEN = "5810449448:AAHiFZR1N-ZaXZ3Ipa9GKseAeal-E9NQeig"

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'show_data'])
def greetings(message):
    reply = "Hi! I'm a simple data collection bot"
    bot.reply_to(message, reply)

    if message.text == '/show_data':
        data = read_data_from_db()
        for datum in data:
            bot.reply_to(message, str(datum))


is_taking_name = False
is_taking_surname = False
user_name = None
surname = None
@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    global is_taking_name
    global is_taking_surname
    global user_name
    global surname

    if is_taking_surname == True:
        surname = message.text
        print(surname)
        is_taking_surname = False
        save_data_to_db(user_name, surname)

    if is_taking_name:
        user_name = message.text
        print(user_name)
        is_taking_name = False
        is_taking_surname = True
        bot.send_message(chat_id, "Input your Surname:")

    if message.text == 'Save name':
        is_taking_name = True
        bot.send_message(chat_id, "Input your Name:")


def save_data_to_db(name, surname):

    connection = None

    try:
        connection = sqlite3.connect("botdatabase")
        cursor = connection.cursor()

        inser_sql =n  f"""INSERT INTO
                    User (name, surname) 
                    VALUES ('{name}', '{surname}')"""

        cursor.execute(inser_sql)
        connection.commit()
        connection.close()

    except Exception as e:
        print("There was an error in the database!")


def read_data_from_db():
    try:
        connection = sqlite3.connect("botdatabase")
        cursor = connection.cursor()

        select_sql = """
        SELECT * FROM User
        """
        cursor.execute(select_sql)
        connection.commit()

        data = cursor.fetchall()

        connection.close()
        return data

    except Exception as e:
        print("There was an error with database!")
        print(e)


bot.infinity_polling()