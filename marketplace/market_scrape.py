import requests
from bs4 import BeautifulSoup
import re

release_id = '3765441'
url = f"https://www.discogs.com/sell/release/{release_id}?output=rss"
response = requests.get(url)
soup = BeautifulSoup(response.content, features="xml")

# NOTE: SKIP THE FIRST "LINK", it's the rss get link
summaries = soup.findAll('summary')
links = soup.findAll('link')  

messy_list = []

# so we're gonna use smthg like this
for i in range(len(summaries)):
    messy_list.append(str(summaries[i].text) + str(links[i+1]))
# note: gotta strip 'USD 16.00' or 'EUR 18.50' and parse
# and get the 'href' outta the link tag. maybe BEFORE turning
# to string

# pricematch regex
re.search('... \d\d.\d\d', messy_list[0])

# link regex
re.findall('"([^"]*)"', messy_list[0])
