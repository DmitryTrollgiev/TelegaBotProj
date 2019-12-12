import telebot

API_TOKEN = "908179410:AAGTLbJbC1n6AnLbqq66cfLlQV9YdC48llU"

bot = telebot.TeleBot(API_TOKEN)

users_d = {}

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id not in users_d:
        users_d[message.from_user.id] = {"date": None, "city" : None, "number" : None}

    bot.reply_to(message, "Привет!, данный бот поможет вам узнать расписание фильмов двух киносетей:\n /1 - Расписание сети Киногалактика\n /2 - Расписание сети Киноквартал")

@bot.message_handler(commands=['1'])
def first_cinema_site(message):
    bot.reply_to(message, "*Вы выбрали сеть кинотеатров Киногалактика*")
    users_d[message.from_user.id]["number"] = 1
    bot.reply_to(message, "Введите дату в формате 01.01.2019 для получения расписания сеансов:")
    

@bot.message_handler(commands=['2'])
def secind_cinema_site(message):
    bot.reply_to(message, "*Вы выбрали сеть кинотеатров Киноквартал*")
    users_d[message.from_user.id]["number"] = 2
    bot.reply_to(message, "Введите дату в формате 01.01.2019 для получения расписания сеансов:")

@bot.message_handler(commands=['2'])
def secind_cinema_site(message):
    bot.reply_to(message, "*Вы выбрали сеть кинотеатров Киноквартал*")
    users_d[message.from_user.id]["number"] = 2
    bot.reply_to(message, "Введите дату в формате 01.01.2019 для получения расписания сеансов:")


# Ввод даты
@bot.message_handler(func=lambda message: True)
def check_date(message):
    if message.from_user.id in users_d:
        bot.reply_to(message, "РАБОТАЕМ")

bot.polling()