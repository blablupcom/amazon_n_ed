from datetime import datetime
from bs4 import BeautifulSoup as bs
import unirest
import scraperwiki
import re


user_agent = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}


with open('test.txt') as f:    # open test.txt file containing the list of url
        url_empty = set()
        for url in f.xreadlines():      # read every line of the file
            try:
                pages = unirest.get(url.strip(), headers = user_agent)    # make a request to the url
            except: continue
            soup = bs(pages.raw_body)
            title =  soup.find('title').text.encode('utf-8')
            print title
            tag = soup.find(text = re.compile('There is a newer edition of this item'))  # find the text on the page
            todays_date = str(datetime.now())
            if tag:                                                                      # if text found
                newed_asin = tag.find_next('a')['href'].split('dp/')[1].split('/')[0]    # get asin of a new edition
                asin = url.split('dp/')[-1]                                              # get asin of the previous edition
                flag_asin = ''
                if url in url_empty:          # if the url is in the set of the urls with no text on the page
                    flag_asin = newed_asin    # get asin and set the flag
                    url_empty.remove(url)     # remove the url from the set
                print asin
            else:
                url_empty.add(url)            # if no text on the page, add the url to the set
                asin = url.split('dp/')[-1]
                newed_asin = ''
                flag_asin = 'there is no a newer edition of this item'   # set the flag that there is no a newer edition of this item
                print flag_asin
            scraperwiki.sqlite.save(unique_keys=['asin'], data={"asin": asin, "new_edition_asin": newed_asin, "flag": flag_asin, "d": todays_date })  # save data into sql database

