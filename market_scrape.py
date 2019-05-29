import requests
from bs4 import BeautifulSoup
import re

release_id = '3765441'
url = f"https://www.discogs.com/sell/release/{release_id}?output=rss"
response = requests.get(url)
soup = BeautifulSoup(response.content, features="xml")

# grab all the summaries and links from discogs marketplace,
# put 'em in a list
messy_list = []
summaries = soup.findAll('summary')
links = soup.findAll('link')  

for i in range(len(summaries)):
    messy_list.append(str(summaries[i].text) + str(links[i+1]))

# reorganize and regex into a list of dicts
release_info = []

for i in range(len(messy_list)):
    this_dict = {}
    this_dict['price'] = re.findall('... \d\d.\d\d', messy_list[i])
    this_dict['url'] = re.findall('"([^"]*)"', messy_list[i])
    this_dict['comment'] = re.findall('\-.*\<',messy_list[i])
    # turn to string and trim some fluff
    this_dict['comment'] = str(this_dict['comment'])
    this_dict['comment'] = this_dict['comment'][4:-3]
    release_info.append(this_dict)

