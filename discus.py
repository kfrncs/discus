# If you're erroring out on this, read my_token.py
from data.my_token import my_token, my_collection, my_wantlist

# imports for data science and API requests
import numpy as np
import pandas as pd
import time
import requests

# grab collections as indicated by my_token.py 
mine = pd.read_csv(my_collection)
want = pd.read_csv(my_wantlist)

# discogs API URL
d_api = 'https://api.discogs.com/releases'

# TODO: COLUMNS I WANT
# mine:
#   is_master (bool), 
#   master_price, (if i don't already have the master release)
#   community rating (only once),
# wantlist:
#   price_over_time


class fetcher:
    '''
    Class to fetch the info from df by release_id column, 
    passing discogs_field into the request
    '''
    def __init__(self, df):
        '''
        Take the DataFrame passed on instantiation and store in self.df
        self.fetched_list is used to store values before adding to DataFrame
        '''
        self.fetched_list = []
        self.df = df


    def fetch_json(self, i, discogs_field):
        json_raw = requests.get(f"{d_api}/{self.df.release_id[i]}/{discogs_field}",
                                params={'token': my_token})
        self.fetched_list.append(json_raw.json())
        pass
   

    def find(self, discogs_field):
        for i in range(len(self.df['release_id'])):
            if (i % 59 == 0 and i != 0):
                self.fetch_json(i, discogs_field)
                print(f'looking at: {self.df.iloc[i]["Title"]} by {self.df.iloc[i]["Artist"]}')
                for second in range(1,60):
                    time.sleep(1)
                    print(f'sleeping {second}')
                    pass
            else:
                self.fetch_json(i, discogs_field)
                print(f'looking at: {self.df.iloc[i]["Title"]} by {self.df.iloc[i]["Artist"]}')
        pass

########## just to test the class
myfetch = fetcher(mine)
# wantfetch = fetcher(want)
myfetch.find('rating')


##### OLD STUFF DOWN HERE

def ratings_by_release(df):
    ratings_list = []
    for i in range(len(df['release_id'])):
        if(i % 59 == 0):
            # wait for Discogs API cap
            time.sleep(60)
            # fetch JSON for each release ID
            json_raw = requests.get(f"https://api.discogs.com/releases/{df.release_id[i]}/rating",
                               params={'token': ''})
             # dig into the returned JSON object for the rating, append it to our list
            ratings_list.append(json_raw.json()['rating']['average'])
        else:
            # same as above, but no waiting
            json_raw = requests.get(f"https://api.discogs.com/releases/{df.release_id[i]}/rating",
                               params={'token': ''})
            ratings_list.append(json_raw.json()['rating']['average'])
    return ratings_list

# my_records_rated = ratings_by_release(mine)
# want_list_rated = ratings_by_release(want)

# mine['rating'] = my_records_rated
# want['rating'] = want_list_rated

# save those CSV's cuz that function takes FOREVER
# mine.to_csv('kfrncs-collection-20190328-0840.csv')
# want.to_csv('kfrncs-wantlist-20190328-0841.csv')
