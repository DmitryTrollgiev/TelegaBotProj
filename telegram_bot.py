import datetime

import telebot

# Сеть Киногалактика - processor 1
import processor1
# Сеть Киноквартал - processor 2
import processor2

API_TOKEN = "TOKEN"

bot = telebot.TeleBot(API_TOKEN)
users_d = {}


# Обработка старта программы
@bot.message_handler(commands=["start"])
def send_welcome(message):
    users_d[message.from_user.id] = {"date": None, "city": None, "source": None}
    bot.reply_to(message,
                 "Привет!, данный бот поможет вам узнать расписание фильмов двух киносетей\n\nДля начала работы выбери киносеть из списка:\n/kinogalactika - сеть кинотеатров Киногалактика\n/kinokvartal - сеть кинотеатров Киноквартал\n")


@bot.message_handler(commands=["kinogalactika"])
def kinogalactika(message):
    if message.from_user.id not in users_d:
        users_d[message.from_user.id] = {"date": None, "city": None, "source": None}
    users_d[message.from_user.id]["source"] = 1
    bot.reply_to(message,
                 "Выбранная вами киносеть - https://kino-galaktika.ru/\nДля начала работы выберите город из списка:\n/cheboksari\n/odintsovo\n/lytkarino")


@bot.message_handler(commands=["kinokvartal"])
def kinokvartal(message):
    if message.from_user.id not in users_d:
        users_d[message.from_user.id] = {"date": None, "city": None, "source": None}
    users_d[message.from_user.id]["source"] = 2
    bot.reply_to(message,
                 "Выбранная вами киносеть - https://киноквартал.рф\nДля начала работы выберите город из списка:\n/irkutsk")


# Ввод города
@bot.message_handler(commands=["cheboksari", "odintsovo", "lytkarino"])
def kinogalactika_check_city(message):
    if message.from_user.id in users_d and users_d[message.from_user.id]["source"] == 1:
        date_now = datetime.datetime.today() + datetime.timedelta(days=1)
        date_now = date_now.strftime('%d.%m.%Y')

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

        bot.reply_to(message, "Выбранная вами киносеть - Киногалактика\nВыбранный вами город - " + rus_city_dict[
            message.text] + "\nВведите дату в формате " + date_now + " для получения расписания сеансов")


@bot.message_handler(commands=["irkutsk"])
def kinokvartal_check_city(message):
    if message.from_user.id in users_d and users_d[message.from_user.id]["source"] == 2:
        date_now = datetime.datetime.today() + datetime.timedelta(days=1)
        date_now = date_now.strftime('%d.%m.%Y')

        city_dict = {
            "/irkutsk": "irkutsk",
        }

        rus_city_dict = {
            "/irkutsk": "Иркутск",
        }

        city = city_dict[message.text]
        users_d[message.from_user.id]["city"] = city

        bot.reply_to(message, "Выбранная вами киносеть - Киноквартал\nВыбранный вами город - " + rus_city_dict[
            message.text] + "\nВведите дату в формате " + date_now + " для получения расписания сеансов")


# Ввод даты
@bot.message_handler(func=lambda message: True)
def check_date(message):
    if message.from_user.id in users_d and users_d[message.from_user.id]["city"] != None and \
            users_d[message.from_user.id]["source"] != None:
        current_city = users_d[message.from_user.id]["city"]
        current_date = message.text
        date = current_date.split(".")
        new_date = date[2] + "/" + date[1] + "/" + date[0]
        users_d[message.from_user.id]["date"] = new_date
        bot.reply_to(message, "Подождите..")

        # Если выбран источник №1 - работа парсера и там же отдаются сообщения пользователю
        if users_d[message.from_user.id]["source"] == 1:
            processor1.html_parser(bot, message, new_date, current_city)
        # Если выбран источник №2 - только работа парсера (сообщения отдаются в этом модуле)
        elif users_d[message.from_user.id]["source"] == 2:
            results = processor2.html_parser(new_date, current_city)
            for result in results:
                bot.reply_to(message, result, parse_mode='HTML')

    # Когда всё выполнили - удаляем элемент из словаря (чтоб пользователь не мог вводить промежуточные команды)
    users_d.pop(message.from_user.id, None)


bot.polling()
