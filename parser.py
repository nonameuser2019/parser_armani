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


count_photo = 0
proxy = {'HTTPS': '163.172.182.164:3128'}
ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}


def create_dir_name():
    dir_name = 'images'
    try:
        os.mkdir(dir_name)
    except OSError:
        print('Папка существует')
    return dir_name


def get_photo(name_photo, dir_name):
    image_list = []
    img_name = []
    image_list.append(name_photo + '_13_a.jpg')
    image_list.append(name_photo + '_13_b.jpg')
    image_list.append(name_photo + '_13_r.jpg')
    image_list.append(name_photo + '_13_d.jpg')
    image_list.append(name_photo + '_13_f.jpg')
    image_list.append(name_photo + '_13_e.jpg')
    print(image_list)
    for img in image_list:
        try:
            global count_photo
            photo_name = count_photo
            file_obj = requests.get(img, stream=True)
            if file_obj.status_code == 200:
                print(file_obj.status_code)
                with open(dir_name+'/'+str(photo_name)+'.jpg', 'bw') as photo:
                    for chunk in file_obj.iter_content(8192):
                        photo.write(chunk)
                count_photo +=1
                img_name.append(str(photo_name))
        except Exception as e:
            print(e)
    return img_name


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




def parser_list(html):
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

        card_url = item.find('a')['href']
        try:
            img = item.find('img', class_='mainImage')['data-origin']
            img_main_photo = img[:img.find('_')]

        except:
            img = item.find('img', class_='mainImage')['src']
            img_main_photo = img[:img.find('_')]

        # вызов функции, которая скачивает все фото и возвращает лист с их именами
        img_name_list = get_photo(img_main_photo, create_dir_name())
        # временная переменная, заменить потом размером
        size = None

        Session = sessionmaker(bind=db_engine)
        session = Session()
        new_element = Armani(product_name, color, full_price, discount_price, product_id, size, ','.join(img_name_list))
        session.add(new_element)
        session.commit()



def main():
    cat_url = 'https://www.armaniexchange.com/us/men/graphictees'
    html = get_html(cat_url)
    page_count = get_page_count(html)
    for count in range(1, page_count +1 ):
        parser_list(get_html(cat_url + '?page=' + str(count)))


if __name__ == '__main__':
    main()
