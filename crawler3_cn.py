import os
import time
import requests
import urllib.parse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

root_url = 'https://uza.uz/cn'
browser = webdriver.Chrome('D:/chromedriver.exe')
browser.get(root_url)
time.sleep(5)
root_soup = BeautifulSoup(browser.page_source, 'html.parser')
lv1_list = [[i.text.strip(), urllib.parse.urljoin(root_url, i['href'])] for i in root_soup.find('div', class_='category-subcategories').find_all('a')]

art_tag_list = []
art_title_list = []
art_url_list = []
art_tag2_list = []
art_time_list = []
art_body_list = []
art_img_list = []

sort_api = 'https://api.uza.uz/api/v1/posts/'
for tag1, url1 in lv1_list:
    print(tag1)
    sort_url = 'https://api.uza.uz/api/v1/posts/' + url1.lstrip('/') + '?page=1&per_page=20&_f=json&_l=cn'
    null = 'null'
    total_num = eval(requests.get(sort_url, timeout=60).text.replace('\/', '/'))['total']
    sort_url = 'https://api.uza.uz/api/v1/posts/' + url1.lstrip('/') + '?page=1&per_page={}&_f=json&_l=cn'.format(total_num)
    items = eval(requests.get(sort_url, timeout=60).text.replace('\/', '/'))['data']
    for item in items:
        art_tag = tag1
        art_title = item['title'].strip()
        art_url = 'https://uza.uz/cn/posts/_{}'.format(item['id'])
        art_tag2 = ''
        art_time = item['publish_time']
        art_body_1 = [item['description']]
        art_body_2 = [i.text for i in BeautifulSoup(item['content'], 'html.parser').find_all('p')]
        art_body = '\n'.join(art_body_1 + art_body_2)
        art_img = [item['files']['thumbnails']['front']['src']]

        art_tag_list.append(tag1)
        art_title_list.append(art_title)
        art_url_list.append(art_url)
        art_tag2_list.append(art_tag2)
        art_time_list.append(art_time)
        art_body_list.append(art_body)
        art_img_list.append(art_img)

data_dict = {'Root': [root_url] * len(art_tag_list), 'Tag1': art_tag_list, 'Tag2': art_tag2_list, 'Url': art_url_list, 'Title': art_title_list, 'Text': art_body_list, 'Time': art_time_list, 'Imgs': art_img_list}
pd.DataFrame.from_dict(data_dict).to_excel('uza.uz_cn.xlsx', index=False)
