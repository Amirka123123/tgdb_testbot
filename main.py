import telebot

TOKEN = "5810449448:AAHiFZR1N-ZaXZ3Ipa9GKseAeal-E9NQeig"

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def greetings(message):
    reply = "Hi! I'm a simple data collection bot"
    bot.reply_to(message, reply)


is_taking_name = False
is_taking_surname = False
is_taking_address = False
@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    global is_taking_name
    global is_taking_surname
    global is_taking_address

    if is_taking_address == True:
        address = message.text
        print(address)
        is_taking_address == False

    if is_taking_surname == True:
        surname = message.text
        print(surname)
        is_taking_surname = False

    if is_taking_name:
        user_name = message.text
        print(user_name)
        is_taking_name = False
        is_taking_surname = True
        bot.send_message(chat_id, "Input your Surname:")
        is_taking_surname = False
        is_taking_address = True
        bot.send_message(chat_id, "Input your Address:")

    if message.text == 'Save name':
        is_taking_name = True
        bot.send_message(chat_id, "Input your Name:")


bot.infinity_polling()