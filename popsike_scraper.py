# TODO todo
# checks if the buttons exist to get min max avg from
# and then saves them against the release_id for each year

# grab the print() statements from discus.py to format search terms

import pandas as pd
from selenium import webdriver
browser = webdriver.Firefox()
import os
from time import sleep

# grab popsike username and password, as well as wantlist
from data.my_token import popsike_user, popsike_password, my_wantlist
want = pd.read_csv(my_wantlist, index_col=False)


# login for popsike
login_url = 'https://www.popsike.com/classes/access_user/login.php'
browser.get(login_url)
username = browser.find_element_by_id("sender-email")
username.clear()
username.send_keys(popsike_user)

password = browser.find_element_by_id("user-pass")
password.clear()
password.send_keys(popsike_password)
browser.find_element_by_name("Submit").click()

# set the release for this loop
release =  [ 'miles', 'davis', 'sketches', 'of', 'spain' ]

# set payload for popsike requests
payload = {
            'url': 'https://www.popsike.com/php/quicksearch.php?',
            'searchtext': '+'.join([word.lower() for word in release]),
            'currsel': str(2), # select currency 2 --> canadian dollars
            'endfrom': None, # start year --> endfrom
            'endthru': None # end year ---> endthru (lol)
        }

# temp list to append info to
release_list = []

years = list(range(2003,2020))
for year in years:
    # set the year to t, reset the local variable price_list
    payload['years'] = year
    price_list = []

    print(f"fetching {payload['years']}")
    page = f"{payload['url']}&searchtext={payload['searchtext']}&currsel={payload['currsel']}&endfrom={year}&endthru={year}"
    print(f'fetching {page}')
    browser.get(page)

    print('sleeping 5s')
    sleep(5)
    # href = browser.find_element_by_xpath(f'/html/body/section/div/div/div[3]/table/tbody/tr[{i}]/td[5]/a')
    button_list = ['/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[3]/a/div/button[1]',
                   '/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[3]/a/div/button[2]',
                   '/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[3]/a/div/button[3]']
    if browser.find_element_by_xpath(button_list[0]):
        print('found buttons, scraping')
        avg_price = browser.find_element_by_xpath(button_list[0])
        min_price = browser.find_element_by_xpath(button_list[1])
        max_price = browser.find_element_by_xpath(button_list[2])
    else:
        print('WARNING: BUTTONS NOT FOUND')
    release_id = 'test_release_id'
    price_list.append(release_id)
    price_list.append(year)
    # REPLACE THESE
    price_list.append('Sketches of Spain')
    price_list.append('Miles Davis')
    price_list.append(avg_price.text)
    price_list.append(min_price.text)
    price_list.append(max_price.text)
    release_list.append(price_list)
    print(f'as of {year}: {release_list}')

def search_query(title, artist):
    return title.lower().split(' ') + album.lower().split(' ')

def popsike_scrape(df):
    """ takes a dataframe built from wantlist csv. returns df with columns:
        [ release_id, title, artist, year, avg_price, min_price, max_price ]
    """
    data = []
    for i in range(len(df['release_id'])):
        payload['searchtext'] = search_query(self.df.iloc[i]["Title"], df.iloc[i]["Artist"])
    return pd.DataFrame.from_records(data)

