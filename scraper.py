from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import scraperwiki
import re


user_agent = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}


with open('test.txt') as f:

        todays_date = ''
        url_empty = set()
        for url in f.readlines():
            try:
                pages = requests.get(url.strip(), headers = user_agent)
            except: continue
            soup = bs(pages.text)
            title =  soup.find('title').text.encode('utf-8')
            print title
            tag = soup.find(text = re.compile('There is a newer edition of this item'))
            if tag:
                newed_asin = tag.find_next('a')['href'].split('dp/')[1].split('/')[0]
                asin = url.split('dp/')[-1]
                flag_asin = ''
                todays_date = str(datetime.now())
                if url in url_empty:
                    flag_asin = url.split('dp/')[1].split('/')[0]
                    url_empty.remove(url)
                print asin
            else:
                url_empty.add(url)
                asin = url.split('dp/')[-1]
                newed_asin = ''
                flag_asin = 'there is no a newer edition of this item'
                print flag_asin
            scraperwiki.sqlite.save(unique_keys=['asin'], data={"asin": asin, "new_edition_asin": newed_asin, "flag": flag_asin, "d": todays_date })

