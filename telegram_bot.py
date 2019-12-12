import json
import telebot
import parser

API_TOKEN = "908179410:AAGTLbJbC1n6AnLbqq66cfLlQV9YdC48llU"

bot = telebot.TeleBot(API_TOKEN)
users_d = {}

def parser_outer(message, jsn):
    d = json.loads(jsn)
    for film in d["films"]:
        out_str = "<b>"+film+"</b>"

        film_timetables = d["films"][film]
        for timetable in film_timetables:
            content = film_timetables[timetable]
            out_str += "\n"+timetable+" - "+content["price"]+" в "+content["type"]
        
        bot.reply_to(message, out_str,parse_mode='HTML')
        print(out_str)


#Обработка старта программы
@bot.message_handler(commands=["start"])
def send_welcome(message):
    if message.from_user.id not in users_d:
        users_d[message.from_user.id] = {"date": None, "city" : None}

    bot.reply_to(message, "Привет!, данный бот поможет вам узнать расписание фильмов сети Киногалактика\n\nДля начала работы введи город из списка:\n/Чебоксары\n/Одинцово\n/Лыткарино")


# Ввод города
@bot.message_handler(commands=["Чебоксары","Одинцово","Лыткарино"])
def check_city(message):
    city_dict = {
        "/Чебоксары" : "cheboksari",
        "/Одинцово" : "odintsovo",
        "/Лыткарино" : "lytkarino", 
    }
    print("message.text",message.text)
    city = city_dict[message.text]
    users_d[message.from_user.id]["city"] = city

    bot.reply_to(message, "Введите дату в формате 12.12.2019 для получения расписания сеансов")

# Ввод даты
@bot.message_handler(func=lambda message: True)
def check_date(message):
    if message.from_user.id in users_d and users_d[message.from_user.id]["city"] != None :
        #try:
        current_city = users_d[message.from_user.id]["city"]
        print("current_city",current_city)
        current_date = message.text
        date = current_date.split(".")
        new_date = date[2]+"/"+date[1]+"/"+date[0]
        users_d[message.from_user.id]["date"] = new_date
        bot.reply_to(message, "Подождите..")
        #Получает JSON от модуля парсера
        result = parser.processing(new_date, current_city)
        #Переводит JSON в красивую строку и отдаёт результат боту
        parser_outer(message, result)
            
        #except:
        #    bot.reply_to(message, "Что-то пошло не та при обработке вашего запроса")

bot.polling()