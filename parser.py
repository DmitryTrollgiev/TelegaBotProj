import json
import requests
from bs4 import BeautifulSoup

def get_site(url):
    r = requests.get(url).text
    return r

def html_parser(date, city):

    #Одинцово
    #sc-1h5tg87-0 duYTXo title
    

    films_dict = {"films": {}, "exception": False}
    #r = get_site("https://kino-galaktika.ru/cinema/?date="+date+"&city="+city+"&facility=kinogalaktika")
    r = get_site("https://kino-galaktika.ru/?date="+date+"&city="+city)
    soup = BeautifulSoup(r, "lxml")

    for link in soup.find_all("div", class_="sc-bdVaJa sc-bwzfXH iPDSpD event-info"):
        #Название фильма
        film_name = link.find("a", class_="event-name").text
        films_dict["films"][film_name] = {}
        print(film_name)

        #Нашли тег с расписанием
        all_timetables = link.find("div",class_="sc-bdVaJa sc-bwzfXH cbFdOh shows")
        
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
                films_dict["films"][film_name][time_list[i]] = {"price": price_list[i], "type": film_type_list[i]}
        else:
            films_dict["exception"] = True

    return films_dict

def to_json(d):
    result_json = json.dumps(d,ensure_ascii=False)
    return result_json

def processing(date, city):
    content = html_parser(date, city)
    return to_json(content)

