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

from data.my_token import popsike_user, popsike_password

release =  [ 'miles', 'davis', 'sketches', 'of', 'spain' ]

payload = {
            'url': 'https://www.popsike.com/php/quicksearch.php?',
            'searchtext': '+'.join([word.lower() for word in release]),
            'currsel': str(2), # select currency 2 --> canadian dollars
            'endfrom': None, # start year --> endfrom
            'endthru': None # end year ---> endthru (lol)
        }

login_url = 'https://www.popsike.com/classes/access_user/login.php'
browser.get(login_url)

username = browser.find_element_by_id("sender-email")
username.clear()
username.send_keys(popsike_user)

password = browser.find_element_by_id("user-pass")
password.clear()
password.send_keys(popsike_password)

browser.find_element_by_name("Submit").click()

test_list = []

# years = list(range(2003,2020))
years = [2003]
for year in years:
    # set the year to t
    payload['years'] = year
    print(f"fetching {payload['years']}")
    page = f"{payload['url']}&searchtext={payload['searchtext']}&currsel={payload['currsel']}&endfrom={year}&endthru={year}"
    print(f'fetching {page}')
    browser.get(page)
    # href = browser.find_element_by_xpath(f'/html/body/section/div/div/div[3]/table/tbody/tr[{i}]/td[5]/a')
    avg_price = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[3]/a/div/button[1]')
    min_price = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[3]/a/div/button[2]')
    max_price = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[3]/a/div/button[3]')
    test_list.append(avg_price.text)
    test_list.append(min_price.text)
    test_list.append(max_price.text)

print(test_list)
