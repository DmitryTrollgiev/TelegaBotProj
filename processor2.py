from bs4 import BeautifulSoup
import requests

def get_site(url):
    """
    Функция получения HTML-кода сайта
    """
    r = requests.get(url).text
    return r


def html_parser():
    
    return_dict = {}
    r = get_site("https://xn--80aaexjbkljxw.xn--p1ai/?date=2019/12/14&city=irkutsk")
    soup = BeautifulSoup(r, "lxml")
    all_films = soup.find_all("div", class_="sc-bdVaJa sc-bwzfXH gYCEQ yf63q6-4 jBxOKw")
    for film in all_films:
        
        #Получаем название фильма
        film_name = film.find("a", class_="event-name").text
        print("\n"+film_name)
        
        #Секция с расписанием
        timetable = film.find("div", class_="sc-bdVaJa sc-bwzfXH iNSiJW schedule")
        times = timetable.find_all("div", class_="sc-bdVaJa sc-bwzfXH sw9zb-2 cDydRB show")
        
        locale_dict = {}
        for time in times:

            #Время начала сеанса
            clock_time = time.find("div", class_="sc-bdVaJa sc-bwzfXH buSbSY").text
            #Цена билета
            price = time.find("div", class_="sc-bdVaJa sc-bwzfXH sw9zb-0 dDMLGB price").text
            #Формат сеанса (Dolby Atmos/3D/2D)
            tformat = time.find("div", class_="sc-bdVaJa sc-bwzfXH gYCEQ sw9zb-1 mZNTg formats").text

            locale_dict[clock_time] = {"price": price, "type": tformat}
        
        return_dict[film_name] = locale_dict
    
    return return_dict

if __name__ == "__main__":
    html_parser()