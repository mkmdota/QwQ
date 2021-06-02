import os
import time
import requests
import urllib.parse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


root_url = 'https://www.inform.kz/cn'
root_soup = BeautifulSoup(requests.get(root_url, timeout=60).text, 'html.parser')
lv1_list = [[i.text.strip(), urllib.parse.urljoin(root_url, i.find('a')['href'])] for i in root_soup.find('nav').find_all('li')]

art_tag_list = []
art_title_list = []
art_url_list = []
art_tag2_list = []
art_time_list = []
art_body_list = []
art_img_list = []

for tag1, url1 in lv1_list:
    print(tag1)
    if url1 == 'https://www.inform.kz/cn/group_g233':
        url1 = 'https://www.inform.kz/cn/section_s23196'

    lv1_soup = BeautifulSoup(requests.get(url1, timeout=60).text, 'html.parser')
    items = lv1_soup.find_all('div', class_='lenta_news_block')
    while len(items) > 0:
        for item in items:
            art_url = urllib.parse.urljoin(root_url, item.find('div', class_='lenta_news_title').find('a')['href'])
            try:
                art_title = item.find('div', class_='lenta_news_title').text.strip()
                art_tag = item.find('div', class_='lenta_news_text').find('div', class_='foot_lenta_b').text.strip().replace('  ', ' ')
                art_time = item.find('div', class_='lenta_news_time-rubric').text.strip()
                art_soup = BeautifulSoup(requests.get(art_url, timeout=60).text, 'html.parser')
                art_body = art_soup.find('div', class_='article_news_body').text.strip()
                art_imgs = [i['src'] for i in art_soup.find('div', class_='article_news_body').find_all('img')]

                art_tag_list.append(tag1)
                art_title_list.append(art_title)
                art_url_list.append(art_url)
                art_tag2_list.append(art_tag)
                art_time_list.append(art_time)
                art_body_list.append(art_body)
                art_img_list.append(art_imgs)
            except Exception as e:
                print(art_url, e)

        final_time = items[-1].find('div', class_='lenta_news_time-rubric').text.strip()
        next_url = '{}?last_id={}-{}-{}%20{}:00'.format(url1, final_time[6:10], final_time[3:5], final_time[0:2], final_time[11:16])
        next_soup = BeautifulSoup(requests.get(next_url, timeout=60).text, 'html.parser')
        items = next_soup.find_all('div', class_='lenta_news_block')

data_dict = {'Root': [root_url] * len(art_tag_list), 'Tag1': art_tag_list, 'Tag2': art_tag2_list, 'Url': art_url_list, 'Title': art_title_list, 'Text': art_body_list, 'Time': art_time_list, 'Imgs': art_img_list}
pd.DataFrame.from_dict(data_dict).to_excel('inform.kz_cn.xlsx', index=False)
