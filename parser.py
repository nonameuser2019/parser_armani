import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import random
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Float
from model import *


proxy = {'HTTPS': '163.172.182.164:3128'}
ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}


def get_html(url, payload=None):
    while True:
        time.sleep(random.randint(random.randint(1, 4), random.randint(5, 8)))
        html = requests.get(url, headers=HEADERS, proxies=proxy, params=None)
        if html.status_code == 200:
            print(html.status_code)
            return html
        elif html.status_code == 403:
            print(html.status_code)
            print('weit to 60 sec')
            time.sleep(60)
        else:
            time.sleep(random.randint(14, 27))
            print(html.status_code)
            continue


def get_page_count(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        page_count = soup.find('ul', class_='pagesWrapper').find('li', class_='lastPage').text
        return int(page_count)
    except:
        page_count = None
        print('Error page count not defined')


def parser_card(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        section = soup.find('main', id='main').find_all('article', class_='item')
    except:
        pass
    for item in section:
        itm = item['data-ytos-track-product-data']
        try:
            product_name = ''.join(itm.split(',')[2][17:-1])
        except:
            product_name = None
        try:
            color = ''.join(itm.split(',')[9][17:-1])
        except:
            color = None
        try:
            full_price = ''.join(itm.split(',')[11][16:])
        except:
            full_price = None
        try:
            discount_price = ''.join(itm.split(',')[12][26:])
        except:
            discount_price = None
        try:
            product_id = ''.join(itm.split(',')[1][17:-1])
        except:
            product_id = None

        # временная переменная, заменить потом размером
        size = None

        Session = sessionmaker(bind=db_engine)
        session = Session()
        new_element = Armani(product_name, color, full_price, discount_price, product_id, size)
        session.add(new_element)
        session.commit()



def main():
    html = get_html('https://www.armaniexchange.com/us/men/graphictees?page=1')
    page_count = get_page_count(html)
    print(page_count)
    parser_card(html)


if __name__ == '__main__':
    main()
