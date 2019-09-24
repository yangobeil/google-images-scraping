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
import glob

#---------------------------- Arguments for parser version ------------------

parser = argparse.ArgumentParser()

parser.add_argument('word', help='word to search on google')
parser.add_argument('-d', '--directory')

args = parser.parse_args()

word = args.word
if args.directory:
    directory = args.directory
else:
    directory = None
    
#---------------------------- Function to scrape that can be imported ------------------


def max_label(name, folder):
    '''Find all the files with pattern name_###.* inside the folder and find
     the largest number. Returns 0 if no file with the pattern.'''
     
    path_pattern = os.path.join(folder, name + "_*")
    existing_files = glob.glob(path_pattern)
    if not existing_files:
        biggest_label = 0
    else:
        existing_labels = map(lambda s: int(s.split('_')[-1].split('.')[0]), existing_files)
        biggest_label = max(existing_labels)
    return biggest_label


def extract_image(link, file_name, directory):
    '''Downloads the image in the link and saves is in the directory under the name file_name.
     This is only done if the file is a jpg and if it can be opened.'''
     
    try:
        img = requests.get(link)
        image_path = os.path.join(directory, file_name)
        with open(image_path, 'wb') as image_file:
            if os.path.splitext(image_path)[1] == '.jpg':
                image_file.write(img.content)
        if cv2.imread(image_path) is None:
            os.remove(image_path)
    except:
        pass


def scrape(word, directory=None):
    '''Searches for word in Google images and downloads all the valid jpg images. 
    Files are saved under name_###.jpg in the specified directory (or current is unspecified).'''
    
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    url = 'https://www.google.com/search?q=' + word + '&source=lnms&tbm=isch'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, features="lxml")
    
    if not directory:
        parentdir = os.getcwd()
        directory = os.path.join(parentdir, word)
        if not os.path.exists(directory):
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
    init_label = max_label('image', directory)
    label = init_label + 1    
    
    for i in range(num_images):
        file_name = f'image_{label}.{types[i]}'
        extract_image(links[i], file_name, directory)
        label += 1
        print(f"Found {label - init_label} images for {word}" + " "*10, end="\r")
            
        
if __name__ == '__main__':
    scrape(word, directory)