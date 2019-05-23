# TODO todo
# put a for_loop in here that works through all the years
# checks if the buttons exist to get min max avg from
# and then saves them against the release_id for each year

# grab the selenium stuff from bbc scraper
# grab the print() statements from discus.py to format search terms

# get dotenv file going

from selenium import webdriver
browser = webdriver.Firefox()
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# load Popsike password from .env
POPS_PASSWORD = os.environ['POPS_PASSWORD']   

release =  [ 'miles', 'davis', 'sketches', 'of', 'spain' ]

payload = {
            'url': 'https://www.popsike.com/php/quicksearch.php?',
            # here be pseudocode
            'searchtext': '+'.join([word.lower() for word in release]),
            # ^^^^ PSEUDOCODE FIX ME ^^^^
            'currsel': str(2), # select currency 2 --> canadian dollars
            'endfrom': None, # start year --> endfrom
            'endthru': None # end year ---> endthru (lol)
        }


years = list(range(2003,2020))
for year in years:
    # set the year to t
    payload['years'] = year
    print(f"fetching {payload['years']}")
    page = f"{payload['url']}&searchtext={payload['searchtext']}&currsel={payload['currsel']}&endfrom={year}&endthru={year}"
    print(f'fetching {page}')
    browser.get(page)
    # href = browser.find_element_by_xpath(f'/html/body/section/div/div/div[3]/table/tbody/tr[{i}]/td[5]/a')



