import json
import requests
from bs4 import BeautifulSoup

def get_site(url):
    r = requests.get(url).text
    return r

def html_parser(date):

    results_d = {}
    r = get_site("https://kino-galaktika.ru/cinema/?date="+date+"&city=lytkarino&facility=kinogalaktika")
    soup = BeautifulSoup(r, "lxml")
    for link in soup.find_all("a", class_="event-name"):
        print(link)

    for link in soup.find_all("div", class_="sc-bdVaJa sc-bwzfXH iPDSpD event-info"):
        print(link.find_all("a", class_="event-name"))
    
    return results_d

def to_json(d):
    result_json = json.dumps(d)
    return result_json

def processing(date):
    content = html_parser(date)
    return to_json(content)
