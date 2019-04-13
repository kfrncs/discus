from my_token import my_token, my_collection, my_wantlist

import numpy as np
import pandas as pd
import time
import requests


mine = pd.read_csv(my_collection)
want = pd.read_csv(my_wantlist)


class fetcher:
    '''fetch the info from df by release_id column, passing discogs_field into the request'''
    
    def __init__(self, df):
        self.fetched_list = []
        self.df = df
    

    def fetch_json(self, i):
        # json_raw = requests.get(f"https://api.discogs.com/releases/{df.release_id[i]}/{discogs_field}",
        #                         params={'token': my_token})
        # self.fetched_list.append(json_raw.json())
        print(i)
        pass
   

    def tick(self):
        # for i in range(len(self.df['release_id'])):
        for i in range(1,300):
            if (i % 59 == 0):
                self.fetch_json(i)
                for seconds in range(1,60):
                    print(f'sleeping: {i}')
                    time.sleep(1)
            else:
                self.fetch_json(i)
        pass

### just to test the class
myfetch = fetcher(my_collection)
wantfetch = fetcher(my_wantlist)
myfetch.tick()


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
