import pandas as pd
import os 
from joblib import load

# get list of csv files that exist
csv_list = os.listdir('data/pricefetch')

# import csv files to list of Pandas dataframes
df_list = []
for i in range(len(csv_list)):
    df_list.append(pd.read_csv(f'data/pricefetch/{csv_list[i]}'))

# turn list into one DataFrame
df_discogs = pd.DataFrame()
df_discogs = pd.concat(df_list, sort=False) 

# make "date" column into datetime
df_discogs['date'] = pd.to_datetime(df_discogs['date'])

# drop extra columns -> erroneous index column, currency columns (it's all canadian)
df_discogs = df_discogs.drop(columns=['Unnamed: 0'])
cols = [c for c in df_discogs.columns if c.endswith('currency') != True]
df_discogs = df_discogs[cols]

# rename columns and reset index
df_discogs = df_discogs.rename(index=str, columns={
    'Fair (F).value': 'fair', 'Good (G).value': 'good', 'Good Plus (G+).value': 'good_plus',
    'Mint (M).value': 'mint', 'Near Mint (NM or M-).value': 'near_mint', 'Poor (P).value': 'poor',
    'Very Good (VG).value': 'vg', 'Very Good Plus (VG+).value': 'vg_plus', 'date': 'date',
    'release_id': 'release_id'})
df_discogs = df_discogs.reset_index()

# reorder columns
df_discogs = df_discogs[['date', 'release_id', 'poor','fair', 'good', 'good_plus', 'vg', 'vg_plus', 'near_mint',  'mint']]

# import popsike-scraped joblib file, put it into a df
list_popsike = load('data/popsike/release_list_may_24.joblib')
df_popsike = pd.DataFrame(list_popsike, columns=['release_id', 'year', 'title', 'artist', 'avg', 'min', 'max'])

# reorder columns on df_popsike
df_popsike = df_popsike[['release_id', 'year', 'title', 'artist', 'min', 'avg', 'max']]

# and get rid of the leading "min", "avg", "max"
df_popsike['min'] = df_popsike['min'].apply(lambda x: x.lstrip('min '))
df_popsike['avg'] = df_popsike['min'].apply(lambda x: x.lstrip('avg '))
df_popsike['max'] = df_popsike['min'].apply(lambda x: x.lstrip('max '))
