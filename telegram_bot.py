import telebot

API_TOKEN = ""

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте, данный бот поможет вам узнать расписание фильмов двух киносетей:\n /1 - Расписание сети Киногалактика\n /2 - Расписание сети киноквартал")

@bot.message_handler(commands=['1'])
def first_cinema_site(message):
    bot.reply_to(message, "Киногалактика")

@bot.message_handler(commands=['2'])
def secind_cinema_site(message):
    bot.reply_to(message, "Киноквартал")

bot.polling()