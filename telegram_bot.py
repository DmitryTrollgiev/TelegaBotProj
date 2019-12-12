import telebot

import parser

API_TOKEN = "TOKEN"

bot = telebot.TeleBot(API_TOKEN)
users_d = {}


# Обработка старта программы
@bot.message_handler(commands=["start"])
def send_welcome(message):
    if message.from_user.id not in users_d:
        users_d[message.from_user.id] = {"date": None, "city": None}

    bot.reply_to(message,
                 "Привет!, данный бот поможет вам узнать расписание фильмов сети Киногалактика\n\nДля начала работы выбери город из списка:\n/cheboksari\n/odintsovo\n/lytkarino")


# Ввод города
@bot.message_handler(commands=["cheboksari", "odintsovo", "lytkarino"])
def check_city(message):
    if message.from_user.id in users_d:
        city_dict = {
            "/cheboksari": "cheboksari",
            "/odintsovo": "odintsovo",
            "/lytkarino": "lytkarino",
        }
        rus_city_dict = {
            "/cheboksari": "Чебоксары",
            "/odintsovo": "Одинцово",
            "/lytkarino": "Лыткарино",
        }

        city = city_dict[message.text]
        users_d[message.from_user.id]["city"] = city

        bot.reply_to(message, "Выбранный вами город - " + rus_city_dict[
            message.text] + "\nВведите дату в формате 12.12.2019 для получения расписания сеансов")


# Ввод даты
@bot.message_handler(func=lambda message: True)
def check_date(message):
    if message.from_user.id in users_d and users_d[message.from_user.id]["city"] != None:
        current_city = users_d[message.from_user.id]["city"]
        current_date = message.text
        date = current_date.split(".")
        new_date = date[2] + "/" + date[1] + "/" + date[0]
        users_d[message.from_user.id]["date"] = new_date
        bot.reply_to(message, "Подождите..")
        # Работа парсера + там же отдаются сообщения пользователю
        parser.html_parser(bot, message, new_date, current_city)


bot.polling()
