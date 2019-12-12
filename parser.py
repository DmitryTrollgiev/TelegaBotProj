import requests
from bs4 import BeautifulSoup

def get_site(url):
    r = requests.get(url).text
    return r

def parser(html):
    pass








def processing(date, number):
    url = 
    content = get_site(url)
    d = parser(content)