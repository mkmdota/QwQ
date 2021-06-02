import os
import re
import time
import requests
import urllib.parse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


root_url = 'https://24.kg/english/'

art_tag_list = []
art_title_list = []
art_url_list = []
art_tag2_list = []
art_time_list = []
art_body_list = []
art_img_list = []

items = []
page_n = 1
while True:
    new_root_url = 'https://24.kg/english/page_{}/'.format(page_n)
    print(new_root_url)
    new_items = BeautifulSoup(requests.get(new_root_url, timeout=300).text, 'html.parser').find_all('div', class_='one')
    if items == new_items:
        break
    items = new_items
    for item in items:
        art_tag = np.nan
        art_tag2 = np.nan
        art_url = urllib.parse.urljoin(root_url, item.find('a')['href'])
        art_soup = BeautifulSoup(requests.get(art_url, timeout=300).text, 'html.parser')
        art_title = art_soup.find('h1').text.strip()
        art_time = art_soup.find('span', id="article-link").text.strip()
        art_body = '\n'.join([i.text.replace('\xa0', ' ').strip() for i in art_soup.find('div', class_='cont').find_all('p')])
        art_imgs = []
        p = art_soup.find('ul', class_="pwslider")
        if p is not None:
            p_list = [urllib.parse.urljoin(root_url, i['href']) for i in p.find_all('a')]
            art_imgs.extend(p_list)
        v = art_soup.find(attrs={'data-video': re.compile('.*?')})
        if v is not None:
            art_imgs.append(v.find('iframe')['src'].strip().strip('//'))

        art_tag_list.append(art_tag)
        art_title_list.append(art_title)
        art_url_list.append(art_url)
        art_tag2_list.append(art_tag2)
        art_time_list.append(art_time)
        art_body_list.append(art_body)
        if len(art_imgs) > 0:
            art_img_list.append(art_imgs)
        else:
            art_img_list.append([])

        data_dict = {'Root': [root_url] * len(art_tag_list), 'Tag1': art_tag_list, 'Tag2': art_tag2_list,
                     'Url': art_url_list, 'Title': art_title_list, 'Text': art_body_list, 'Time': art_time_list,
                     'Imgs': art_img_list}
        pd.DataFrame.from_dict(data_dict).to_excel('web4/24.kg_en.xlsx', index=False)
    page_n += 1
data_dict = {'Root': [root_url] * len(art_tag_list), 'Tag1': art_tag_list, 'Tag2': art_tag2_list, 'Url': art_url_list, 'Title': art_title_list, 'Text': art_body_list, 'Time': art_time_list, 'Imgs': art_img_list}
pd.DataFrame.from_dict(data_dict).to_excel('web4/24.kg_en.xlsx', index=False)
