import pandas as pd
import os 

# get list of csv files that exist
csv_list = os.listdir('data/pricefetch')

# import csv files to list of Pandas dataframes
df_list = []
for i in range(len(csv_list)):
    df_list.append(pd.read_csv(f'data/pricefetch/{csv_list[i]}'))

# turn list into one DataFrame
df = pd.DataFrame()
df = pd.concat(df_list) 

# make "date" column into datetime
df['date'] = pd.to_datetime(df['date'])

# drop extra columns -> index column, currency columns (it's all canadian)
df = df.drop(columns=['Unnamed: 0'])
cols = [c for c in df.columns if c.endswith('currency') != True]
df = df[cols]

# rename columns
df = df.rename(index=str, columns={
    'Fair (F).value': 'fair', 'Good (G).value': 'good', 'Good Plus (G+).value': 'good_plus',
    'Mint (M).value': 'mint', 'Near Mint (NM or M-).value': 'near_mint', 'Poor (P).value': 'poor',
    'Very Good (VG).value': 'vg', 'Very Good Plus (VG+).value': 'vg_plus', 'date': 'date',
    'release_id': 'id'})

# reorder columns
df = df[['date', 'id', 'poor','fair', 'good', 'good_plus', 'vg', 'vg_plus', 'near_mint',  'mint']]
