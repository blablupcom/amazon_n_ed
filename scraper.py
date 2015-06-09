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

entity_id = "E37"
urls = ["http://www.amazon.com/dp/020559526X",'http://www.amazon.com/dp/0205881394','http://www.amazon.com/dp/0078029546',
'http://www.amazon.com/dp/0132729822']
user_agent = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
link = ''
todays_date = ''
for url in urls:
         try:
            pages = requests.get(url, headers = user_agent)
         except: continue
         soup = bs(pages.text)
         #print soup
         titles =  soup.find('title').text
         tag = soup.find(text = re.compile('There is a newer edition of this item'))
         if tag:
             url_link = soup.find(text = re.compile('There is a newer edition of this item')).find_next('a')['href']
             #tag = soup.find('div', attrs = {'id', 'newerVersion_feature_div'}).text
             link = 'http://www.amazon.com'+url_link
             todays_date = str(datetime.now())
             print link
         else:
             link = 'there is no a newer edition of this item'
             print link
         filename = entity_id + "_" +  ".csv"
         scraperwiki.sqlite.save(unique_keys=['l'], data={"l": link, "f": url, "d": todays_date })
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
