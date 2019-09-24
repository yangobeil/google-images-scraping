# google-images-scraping
Scrape automatically google images for a given key word and saves all the jpg images obtained. The libraries needed to run the code are BeautifulSoup, os, OpenCV, requests, glob, argparse and json. 

The code can be used directly from the command line by going to the directory where the code is and running

```
python scraper.py word -d directory
```

The word is the query and the directory is an option to specify where to save the images. If no directoy is specified the program creates a directory called word. The images are names image_###.jpg and the numbering starts where the already existing files stop.

It is also possible to import the function 'scrape' into another script to run the scraper. The arguments are the same as before: word and directory (optional).
