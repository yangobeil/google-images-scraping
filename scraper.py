# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:14:56 2019

@author: Yan
"""

from bs4 import BeautifulSoup
import os
import requests
import json

word = 'cat'
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
url = 'https://www.google.com/search?q=' + word + '&source=lnms&tbm=isch'
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, features="lxml")

directory = 'C:\\Users\\Yan\\Dropbox\\Machine learning\\images google'

links = []
types = []
for image in soup.find_all('div', {'class':'rg_meta'}):
    link = json.loads(image.text)['ou']
    type = json.loads(image.text)['ity']
    if type:
        links.append(link)
        types.append(type)

num_images = len(links)

for i in range(num_images):
    img = requests.get(links[i])
    file_name = str(i) + '.' + types[i]
    path = os.path.join(directory, file_name)
    with open(path, 'wb') as image_file:
        image_file.write(img.content)