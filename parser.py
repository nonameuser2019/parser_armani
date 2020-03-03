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


cat_name_list = []
product_id_list = []
cat_url_list = []
sizes_list = []
colors_list = []
datails_list = []
count_photo = 0
proxy = {'HTTPS': '163.172.182.164:3128'}
ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}
API_URL = 'https://www.armaniexchange.com/yTos/api/Plugins/ItemPluginApi/GetCombinationsAsync/?siteCode=ARMANIEXCHANGE_US'
Session = sessionmaker(bind=db_engine)
session = Session()


def create_dir_name():
    dir_name = 'images'
    try:
        os.mkdir(dir_name)
    except OSError:
        print('Папка существует')
    return dir_name


def read_file_url():
    with open('input.txt', 'r') as file:
        for line in file:
            cat_url_list.append(line.strip('\n'))
    return cat_url_list


def get_photo(name_photo, dir_name):
    image_list = []
    img_name = []
    image_list.append(name_photo + '_13_a.jpg')
    image_list.append(name_photo + '_13_b.jpg')
    image_list.append(name_photo + '_13_r.jpg')
    image_list.append(name_photo + '_13_d.jpg')
    image_list.append(name_photo + '_13_f.jpg')
    image_list.append(name_photo + '_13_e.jpg')
    for img in image_list:
        try:
            global count_photo
            photo_name = count_photo
            file_obj = requests.get(img, stream=True)
            if file_obj.status_code == 200:
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


def get_parse_card(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        catagery_lst = soup.find('ul', class_='breadcrumbs').find_all('li')
        cat_name = catagery_lst[1].text + '/' + catagery_lst[2].text + '/' + catagery_lst[3].text
    except Exception as e:
        print(e)
        print('cat_name')
        cat_name = ''
    try:
        name = soup.find('span', class_='modelName inner').text
    except Exception as e:
        name = soup.find('span', class_='microCategory').text
    try:
        details = soup.find('div', class_='details').find('ul').find_all('li')
        for li in details:
             datails_list.append(li.text)
    except Exception as e:
        datails_list.append(None)
    try:
        card_id = soup.find('div', class_='details').find('ul').find_all('li')[-1].text
    except:
        card_id = None
    return name, datails_list, cat_name, card_id


def get_page_count(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        page_count = soup.find('ul', class_='pagesWrapper').find('li', class_='lastPage').text
        return int(page_count)
    except:
        pass
        try:
            page_count = soup.find('ul', class_='pagesWrapper').find_all('li', class_='')[-1].text.strip()
            return int(page_count)
        except:
            print('page_cont = 0')
            return 0


def parser_list(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    url = html.url
    try:
        section = soup.find('main', id='main').find_all('article', class_='item')
    except:
        pass
    for item in section:
        try:
            card_url = item.find('a')['href']
        except Exception as e:
            card_url = None

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



        try:
            img = item.find('img', class_='mainImage')['data-origin']
            img_main_photo = img[:img.find('_')]

        except:
            img = item.find('img', class_='mainImage')['src']
            img_main_photo = img[:img.find('_')]

        try:
            # копируем ид всех цветов обьявлений по которым можно потом свести товары
            all_color = item.find('a', class_='more-colors-label')['data-store-opt']
            data = json.loads(all_color)['options']['data']['ItemImage']
            for code in data:
                product_id_list.append(code['Code10'])
        except:
            pass

        # вызов функции, которая скачивает все фото и возвращает лист с их именами
        img_name_list = get_photo(img_main_photo, create_dir_name())

        payload = {
            'code10': product_id
        }
        response = requests.get(API_URL, proxies=proxy, headers=HEADERS, params=payload)
        if response.status_code == 200:
            for colors in response.json()['Colors']:
                colors_list.append(colors['Description'])
            for size in response.json()['ModelColorSizes']:
                if size['Color']['Code10'] == product_id:
                    sizes_list.append(size['Size']['Description'])
        else:
            colors_list.append('None')
            sizes_list.append('None')
        try:
            # парсинг категории
            category = soup.find_all('li', class_='crumb')
            for li in category[1:]:
                cat_name_list.append(li.find('span', class_='text').text)
        except:
            pass
        product_name, datails_list, cat_name, card_id = get_parse_card(get_html(card_url))
        try:
            new_element = Armani(product_name, color, full_price, discount_price, product_id, ','.join(img_name_list),
                                 ','.join(sizes_list), ','.join(colors_list), ','.join(datails_list), ','.join(cat_name_list), card_url, ','.join(product_id_list))
            session.add(new_element)
            session.commit()
        except:
            try:
                with open('error.txt', 'a') as read_file:
                    read_file.writelines(f'Url: {card_url} id card: {card_id} \n')
            except:
                pass
        sizes_list.clear()
        colors_list.clear()
        datails_list.clear()
        product_id_list.clear()
        cat_name_list.clear()


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
