import os
import time
import requests
import urllib.parse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


root_url = 'https://www.kazpravda.kz/en'
root_soup = BeautifulSoup(requests.get(root_url, timeout=60).text, 'html.parser')
lv1_list = [[i.text.strip(), urllib.parse.urljoin(root_url, i.find('a')['href'])] for i in root_soup.find('ul', class_='main_rubrics').find_all('li')]

art_tag_list = []
art_title_list = []
art_url_list = []
art_tag2_list = []
art_time_list = []
art_body_list = []
art_img_list = []

for tag1, url1 in lv1_list:
    print(tag1)
    page = 1
    while 1:
        sort_url = '{}/page-{}/'.format(url1, page)
        lv1_soup = BeautifulSoup(requests.get(sort_url, timeout=60).text, 'html.parser')
        items = lv1_soup.find_all('div', class_='today__container')
        if len(items) == 0:
            break

        for item in items:
            art_url = urllib.parse.urljoin(root_url, item.find('a')['href'])
            try:
                art_tag = tag1
                art_title = item.find('h2').text.strip()
                art_tag2 = ''
                art_soup = BeautifulSoup(requests.get(art_url, timeout=60).text, 'html.parser')
                art_time = art_soup.find('div', class_='author_date_article').text.strip()
                art_body = art_soup.find('div', class_='article_text_block').text.strip()
                art_imgs1 = [urllib.parse.urljoin(art_url, i['src']) for i in art_soup.find('div', class_='article_img_block gallery gallery-hover').find_all('img')]
                art_imgs2 = [urllib.parse.urljoin(art_url, i['src']) for i in art_soup.find('div', class_='article_text_block').find_all('img')]
                art_imgs = art_imgs1 + art_imgs2

                art_tag_list.append(tag1)
                art_title_list.append(art_title)
                art_url_list.append(art_url)
                art_tag2_list.append(art_tag2)
                art_time_list.append(art_time)
                art_body_list.append(art_body)
                art_img_list.append(art_imgs)
            except Exception as e:
                print(art_url, e)
        page += 1

data_dict = {'Root': [root_url] * len(art_tag_list), 'Tag1': art_tag_list, 'Tag2': art_tag2_list, 'Url': art_url_list, 'Title': art_title_list, 'Text': art_body_list, 'Time': art_time_list, 'Imgs': art_img_list}
pd.DataFrame.from_dict(data_dict).to_excel('kazpravda.kz_en.xlsx', index=False)

