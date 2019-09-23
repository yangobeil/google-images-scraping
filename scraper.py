# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:14:56 2019

@author: Yan
"""

# based off https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57
# and https://www.pyimagesearch.com/2017/12/04/how-to-create-a-deep-learning-dataset-using-google-images/
from bs4 import BeautifulSoup
import os
import requests
import json
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('word', help='word to search on google')
parser.add_argument('-d', '--directory')

args = parser.parse_args()

word = args.word
if args.directory:
    parentdir = args.directory
else:
    parentdir = None

def scrape(word, parentdir=None):
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    url = 'https://www.google.com/search?q=' + word + '&source=lnms&tbm=isch'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, features="lxml")
    
    if not parentdir:
        parentdir = os.getcwd()
    directory = os.path.join(parentdir, word)
    os.mkdir(directory)
    
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
        image_path = os.path.join(directory, file_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(img.content)
        if cv2.imread(image_path) is None:
            os.remove(image_path)
            
if __name__ == '__main__':
    scrape(word, parentdir)