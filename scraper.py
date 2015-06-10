from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import scraperwiki
import re


user_agent = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}


def amazon_req(titles, asin, newed_asin, flag_asin, todays_date):
    url_empty = set()
    for url in f.readlines():
        print url
        try:
             pages = requests.get(url.strip(), headers = user_agent)
        except: continue
        soup = bs(pages.text)
        titles =  soup.find('title').text
        tag = soup.find(text = re.compile('There is a newer edition of this item'))
        if tag:
            newed_asin = tag.find_next('a')['href'].split('dp/')[1].split('/')[0]
            if url in url_empty:
                flag_asin = url.split('dp/')[1].split('/')[0]
                url_empty.remove(url)
            asin = url.split('dp/')[-1]
            todays_date = str(datetime.now())
            print asin, newed_asin
        else:
            url_empty.add(url)
            flag_asin = 'there is no a newer edition of this item'
            print flag_asin
        return titles, asin, newed_asin, flag_asin, todays_date


if __name__ == '__main__':
    with open(' test.txt') as f:
        titles = ''
        todays_date = ''
        asin = ''
        newed_asin = ''
        flag_asin = ''
        titles, asin, newed_asin, flag_asin, todays_date = amazon_req(titles, asin, newed_asin, flag_asin, todays_date )
        scraperwiki.sqlite.save(unique_keys=['a'], data={"a": asin, "flag": flag_asin, "d": todays_date })
        while titles == 'Robot Check':
            titles, asin, newed_asin, flag_asin, todays_date = amazon_req(titles, asin, newed_asin, flag_asin, todays_date )
            scraperwiki.sqlite.save(unique_keys=['asin'], data={"asin": asin, "new_edition_asin": newed_asin,"flag": flag_asin, "date": todays_date })
