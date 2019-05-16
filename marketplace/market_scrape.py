import requests
from bs4 import BeautifulSoup

release_id = '3765441'
url = f"https://www.discogs.com/sell/release/{release_id}?output=rss"
response = requests.get(url)
soup = BeautifulSoup(response.content, features="xml")
items = soup.findAll('summary')

# note: capture URL/listing id as well
for i in range(len(items)):
    items[i] = items[i].text
