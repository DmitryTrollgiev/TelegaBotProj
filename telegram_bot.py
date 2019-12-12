import json
import telebot
import parser

API_TOKEN = "908179410:AAGTLbJbC1n6AnLbqq66cfLlQV9YdC48llU"

bot = telebot.TeleBot(API_TOKEN)
users_d = {}

def parser_formater(jsn):
    d = json.loads(jsn)
    return d

#Обработка старта программы
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id not in users_d:
        users_d[message.from_user.id] = {"date": None, }

    bot.reply_to(message, "Привет!, данный бот поможет вам узнать расписание фильмов сети Киногалактика\nДля начала работы введите дату в формате 01.01.2019 для получения расписания сеансов")

# Ввод даты
@bot.message_handler(func=lambda message: True)
def check_date(message):
    if message.from_user.id in users_d:
        try:
            current_date = message.text
            date = current_date.split(".")
            new_date = date[2]+"/"+date[1]+"/"+date[0]
            users_d[message.from_user.id]["date"] = new_date
            bot.reply_to(message, "Подождите..")
            #Получает JSON от модуля парсера
            result = parser.processing(new_date)
            #Переводит JSON в красивую строку
            formated_result = parser_formater(result)
            #Отдаёт результат боту
            bot.reply_to(message, formated_result)
        except:
            bot.reply_to(message, "Неверный формат ввода даты!")

bot.polling()