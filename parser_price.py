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
import os


sizes_list = []
cat_url_list = []
proxy = {'HTTPS': '163.172.182.164:3128'}
ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}
API_URL = 'https://www.armaniexchange.com/yTos/api/Plugins/ItemPluginApi/GetCombinationsAsync/?siteCode=ARMANIEXCHANGE_US'


def read_file_url():
    with open('input.txt', 'r') as file:
        for line in file:
            cat_url_list.append(line.strip('\n'))
    return cat_url_list


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
        print('Error page count not defined')
        try:
            page_count = soup.find('ul', class_='pagesWrapper').find_all('li', class_='')[-1].text.strip()
            return int(page_count)
        except:
            print('page_cont = 0')
            return 0


def parser_list(html):
    global product_id
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        section = soup.find('main', id='main').find_all('article', class_='item')
    except:
        pass
    for item in section:
        itm = item['data-ytos-track-product-data'].split(',')
        for i in itm:
            if i.find('product_price_tf') != -1:
                full_price = i[19:]

            if i.find('product_cod10') != -1:
                product_id = i[17:-1]

            if i.find('product_color') != -1 and i.find('product_color_id') == -1:
                color = i[17:-1]

            if i.find('product_discountedPrice_tf') != -1:
                discount_price = i[29:]
        payload = {
            'code10': product_id
        }
        response = requests.get(API_URL, proxies=proxy, headers=HEADERS, params=payload)
        if response.status_code == 200:
            for size in response.json()['ModelColorSizes']:
                if size['Color']['Code10'] == product_id:
                    sizes_list.append(size['Size']['Description'])
        Session = sessionmaker(bind=db_engine)
        session = Session()
        new_element = ArmaniPrice(color, full_price, discount_price, product_id, ','.join(sizes_list))
        session.add(new_element)
        session.commit()
        sizes_list.clear()

def main():
    cat_url_list = read_file_url()
    for cat_url in cat_url_list:
        html = get_html(cat_url)
        page_count = get_page_count(html)
        if page_count == 0:
            parser_list(get_html(cat_url + '?page=1'))
        else:
            for count in range(1, page_count + 1):
                parser_list(get_html(cat_url + '?page=' + str(count)))


if __name__ == '__main__':
    main()