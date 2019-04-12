#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import altair as alt
import discogs_client
import requests
import time

# DEFINE THE USER TOKEN
my_user_token =

# import CSV's of the records I own (mine) and the records I want (want)
mine = pd.read_csv('kfrncs-collection-20190328-0840.csv')
want = pd.read_csv('kfrncs-wantlist-20190328-0841.csv')

# cleaning #

def scrub_nulls():
    '''replace 0's in "released" with a null value'''
    mine['released'] = mine['released'].replace(0,np.NaN) 
    want['released'] = want['released'].replace(0,np.NaN)

# turn the "released" columns into pandas datetime values. format=%Y denotes "Year"
def fetch_years():
    mine['released'] = pd.to_datetime(mine['released'], format="%Y")
    want['released'] = pd.to_datetime(mine['released'], format="%Y")



### TODO: probably wanna refactor everything from here on. it would be nice if x_by_release thing was a class
### that had 

def ratings_by_release(df):
    ratings_list = []
    for i in range(len(df['release_id'])):
        if(i % 59 == 0):
            # wait for Discogs API cap
            time.sleep(60)
            # fetch JSON for each release ID
            json_raw = requests.get(f"https://api.discogs.com/releases/{df.release_id[i]}/rating",
                               params={'token': 'ovZnEqFNotnIPnpqwWYkcbwOqOTberpelOQmrZAt'})
             # dig into the returned JSON object for the rating, append it to our list
            ratings_list.append(json_raw.json()['rating']['average'])
        else:
            # same as above, but no waiting
            json_raw = requests.get(f"https://api.discogs.com/releases/{df.release_id[i]}/rating",
                               params={'token': 'ovZnEqFNotnIPnpqwWYkcbwOqOTberpelOQmrZAt'})
            ratings_list.append(json_raw.json()['rating']['average'])
    return ratings_list

my_records_rated = ratings_by_release(mine)
want_list_rated = ratings_by_release(want)

mine['rating'] = my_records_rated
want['rating'] = want_list_rated

# save those CSV's cuz that function takes FOREVER
mine.to_csv('kfrncs-collection-20190328-0840.csv')
want.to_csv('kfrncs-wantlist-20190328-0841.csv')

# replace 0's in "released" with a null value (you can't rate 0 stars, so these are missing data)
mine['rating'] = mine['rating'].replace(0,np.NaN) 
want['rating'] = want['rating'].replace(0,np.NaN)

def price_by_release(df):
    json_list = []
    for i in range(len(df['release_id'])):
        if(i % 59 == 0):
            # Discogs caps at 60 requests per minute. I'm making more than 60 requests so I wait.
            time.sleep(60)
            # fetch JSON for each release ID
            json_raw = requests.get(f"https://api.discogs.com/marketplace/price_suggestions/{df.release_id[i]}",
                               params={'token': 'ovZnEqFNotnIPnpqwWYkcbwOqOTberpelOQmrZAt'})
             # dig into the returned JSON object for the rating, append it to our list
            json_list.append(json_raw.json())
        else:
            # same as above, but no waiting
            json_raw = requests.get(f"https://api.discogs.com/marketplace/price_suggestions/{df.release_id[i]}",
                               params={'token': 'ovZnEqFNotnIPnpqwWYkcbwOqOTberpelOQmrZAt'})
            json_list.append(json_raw.json())
    return json_list

want_price = price_by_release(want)

new_want_price = []

for i in range(len(want_price)):
    if 'Very Good Plus (VG+)' in want_price[i].keys():
        new_want_price.append(want_price[i]['Very Good Plus (VG+)']['value'])
    else:
        new_want_price.append(0)


# Store the VG+ recommended prices into a new column
want['vgp_price'] = new_want_price

# null the zeroes and save it again
want['vgp_price'] = want['vgp_price'].replace(0,np.NaN)
want.to_csv('kfrncs-wantlist-20190328-0841.csv')


