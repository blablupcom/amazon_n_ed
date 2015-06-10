from datetime import datetime
#import urllib
#import BeautifulSoup
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
import csv
#import time
import requests
import scraperwiki
import re
import os

entity_id = "E37"
# urls = ["http://www.amazon.com/dp/020559526X",'http://www.amazon.com/dp/0205881394','http://www.amazon.com/dp/0078029546',
# 'http://www.amazon.com/dp/0132729822','http://www.amazon.com/dp/1618656449','http://www.amazon.com/dp/0132319705', 'http://www.amazon.com/dp/1893858707'
#  ]




user_agent = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
link = ''
todays_date = ''
url_em = ''
flag = ''
filename = 'test.txt'
if os.path.exists(filename):
    # Open the file.
    with open(filename) as f:

#f = open('test.txt', 'r')
#with open('test.txt', 'r') as f:
        url_empty = set()
        for url in f.readline():
                 try:
                    pages = requests.get(url, headers = user_agent)
                 except: continue
                 soup = bs(pages.text)
                 #print soup
                 titles =  soup.find('title').text
                 tag = soup.find(text = re.compile('There is a newer edition of this item'))
                 if tag:
                     url_link = soup.find(text = re.compile('There is a newer edition of this item')).find_next('a')['href']
                     if url in url_empty:
                         flag_asin = url.split('dp/')[1].split('/')[0]
                         url_empty.remove(url)
                     #tag = soup.find('div', attrs = {'id', 'newerVersion_feature_div'}).text
                     link = 'http://www.amazon.com'+url_link
                     asin = url.split('dp/')[-1]
                     todays_date = str(datetime.now())
                     print asin
                 else:
                     url_empty.add(url)
                     link = 'there is no a newer edition of this item'

                     url_em = url
                     print link
                 filename = entity_id + "_" +  ".csv"
                 scraperwiki.sqlite.save(unique_keys=['l'], data={"l": link, "f": url_em, "flag": flag, "d": todays_date })
                 while titles == 'Robot Check':
                     try:
                            pages = requests.get(url, headers = user_agent)
                     except:
                            continue
                     soup = bs(pages.text)
                     print soup
                     titles =  soup.find('title').text
                     tag = soup.find('div', attrs = {'id', 'newerVersion_feature_div'}).find('h4').text
                     print tag
