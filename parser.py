import json
import requests
from bs4 import BeautifulSoup

def get_site(url):
    r = requests.get(url).text
    return r

def html_parser(date):

    films_dict = {}
    r = get_site("https://kino-galaktika.ru/cinema/?date="+date+"&city=lytkarino&facility=kinogalaktika")
    soup = BeautifulSoup(r, "lxml")

    for link in soup.find_all("div", class_="sc-bdVaJa sc-bwzfXH iPDSpD event-info"):
        #Название фильма
        film_name = link.find("a", class_="event-name").text
        films_dict[film_name] = {}
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
        
        print(len(time_list))
        print(len(price_list))

        if len(time_list) == len(price_list):
            for i in range(len(time_list)):
                print(time_list[i],price_list[i])
            
        else:
            print("ОШИБКА НЕ ПОНТНО ЧТО ДЕЛАТЬ")
        


            

        #Расписание



    #for link in soup.find_all("div", class_="sc-bdVaJa sc-bwzfXH iPDSpD event-info"):
    #    print(link.find_all("a", class_="event-name"))
    
    return films_dict

def to_json(d):
    result_json = json.dumps(d)
    return result_json

def processing(date):
    content = html_parser(date)
    return to_json(content)

if __name__ == "__main__":
    processing("13/12/2019")