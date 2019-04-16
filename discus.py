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
d_api = 'https://api.discogs.com/'

####### TODO:
# 
# autobackups
#
# mine:
#   check if it is_master (master, or "best" release, bool), 
#   master_price, (if i don't already have the master release)
#   maybe create my own metadata column to input whether I want a dupe/upgrade?
#
# wantlist:
#   price_over_time
#   my_rating (then I can use the stars in discogs to rank 1-5 how badly I want each record)
#
# marketplace:
#   keep looking for stuff from wantlist or "dupe"list
#   check sellers' inventory for other items from wantlist
#   compare to historical prices
#
#######

class fetcher:
    '''
    Class to fetch the info from df by release_id column, 
    passing discogs_field into the request.
    '''

    def __init__(self, df):
        '''
        Take the DataFrame passed on instantiation and store in self.df
        self.fetched_list is used to store values before adding to DataFrame
        '''
        self.fetched_list = []
        self.df = df

    def fetch_json(self, i, discogs_field):
        '''
        Call requests.get, inheriting the counter i from self.find(), being passed discogs_field
        to determine data requested. Attach JSON data to self.fetched_list.
        '''
        #TODO: turn fetched_list into fetched_dict and make it release_id : JSON object

        # Discogs API request for specified record and field.
        json_raw = requests.get(f"{d_api}/{discogs_field}/{self.df.release_id[i]}",
                                params={'token': my_token})
        # Append to attribute fetched_list
        self.fetched_list.append(json_raw.json())
        return self

    def find(self, discogs_field):
        '''
        Implements sleeper function required to stay beneath Discogs' 60 requests/minute.
        Calls fetch_json, which stores the JSON elements in fetched_list - which still needs to
        be added to Pandas DataFrames with stitch_price(), or other methods designed later to deal
        with other use cases.
        '''
        # iterate through passed DataFrame's release_id column.
        for i in range(len(self.df['release_id'])):
            # TODO: VERIFY THAT THIS LOOP IS NOT CAUSING AN OFF-BY-ONE UPON STITCHING
            if (i % 59 == 0 and i != 0):
                # make the API call
                self.fetch_json(i, discogs_field)
                # keep track of where we are
                print(f'requesting: {self.df.iloc[i]["Title"]} by {self.df.iloc[i]["Artist"]}')
                # sleep
                for second in range(1,60):
                    time.sleep(1)
                    print(f'sleeping {second}')
            else:
                #API calls up to 59, no sleeping. print to keep track of progress.
                self.fetch_json(i, discogs_field)
                print(f'requesting: {self.df.iloc[i]["Title"]} by {self.df.iloc[i]["Artist"]}')
        return self

    def stitch_price(self):
        '''
        TODO
        combines self.fetched_list with corresponding DataFrames 
        '''
        # old code:
        # self.ratings_list.append(json_raw.json()['rating']['average'])
        # which was then tacked onto the DataFrame from the collection/wantlist .csv
        return self


########## just to test the class
myfetch = fetcher(mine)
wantfetch = fetcher(want)
myfetch.find('/marketplace/price_suggestions/')
