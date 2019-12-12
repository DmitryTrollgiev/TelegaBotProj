import json
import requests
from bs4 import BeautifulSoup

def parser_outer(bot, message, jsn, film_name):
    d = json.loads(jsn)
    out_str = "<b>"+film_name+"</b>"
    if d["exception"] == False:
        for timetable in d["info"]:
            content = d["info"][timetable]
            out_str += "\n"+timetable+" - "+content["price"]+" в "+content["type"]
            
        bot.reply_to(message, out_str, parse_mode='HTML')
    else:
        bot.reply_to(message, "<b>"+film_name+"</b>\nОшибка парсинга", parse_mode='HTML')


def get_site(url):
    """
    Функция получения HTML-кода сайта
    """
    r = requests.get(url).text
    return r

def locale_html_parser(url):
    """
    Функция генерации словаря на основе расписания + парсинг сайта
    """
    locale_dict = {}
    #Парсим ссылку с фильмом
    locale_soup = BeautifulSoup(get_site(url), "lxml")
    all_timetables = locale_soup.find("div", class_="sc-bdVaJa sc-bwzfXH iNSiJW schedule")
                
    #Время всех сеансов текущего фильма
    time_list = []
    for time in all_timetables.find_all("div", class_="sc-bdVaJa sc-bwzfXH buSbSY"):
        time_list.append(time.text)
                
    #Цена в руб для всех сеансов текущего фильма
    price_list = []
    for price in all_timetables.find_all("div", class_="sc-bdVaJa sc-bwzfXH sw9zb-0 dDMLGB price"):
        price_list.append(price.text)
                
    #Тип фильма (3D/2D) для всех сенсов текущего фильма
    film_type_list = []
    for film_type in all_timetables.find_all("div", class_="sc-bdVaJa sc-bwzfXH gYCEQ sw9zb-1 jXcRgy formats"):
        film_str = film_type.text
        if film_str == "":
            film_type_list.append("2D")
        elif film_str == "3D":
            film_type_list.append(film_str)
        else:
            film_type_list.append("???")

    if len(time_list) == len(price_list) and len(film_type_list) == len(time_list):
        #Заносим в словарь
        for i in range(len(time_list)):
            locale_dict[time_list[i]] = {"price": price_list[i], "type": film_type_list[i]}
        if locale_dict == {}:
            return {"info": {}, "exception": True}
        return {"info": locale_dict, "exception": False}
    else:
        return {"info": {}, "exception": True}
    
def html_parser(bot, message, date, city):
    """
    Основной генератор-парсер словаря
    """

    URL = "https://kino-galaktika.ru"

    r = get_site(URL+"/?date="+date+"&city="+city)
    soup = BeautifulSoup(r, "lxml")
    
    #Словарь для хранения фильма и ссылки на него
    films_urls = {}
    #Формируем Список всех фильмов
    for link in soup.find_all("h2", class_="sc-1h5tg87-0 duYTXo title"):
        #Находим ссылку на фильм
        for a in link.find_all('a', href=True):
            if "&city="+city in a['href']:
                
                film_name = link.text
                if film_name not in films_urls:
                    films_urls[film_name] = URL+a['href']
                
    #Для каждого фильма получаем расписание в отельной функции    
    for film in films_urls:
        result = locale_html_parser(films_urls[film])
        json_result = to_json(result)
        parser_outer(bot, message, json_result, film)

def to_json(d):
    """
    Перевод в JSON
    """
    result_json = json.dumps(d,ensure_ascii=False)
    return result_json