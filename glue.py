import pandas as pd
import os 

csv_list = os.listdir('data/pricefetch')
df_list = []
master_df = pd.DataFrame()
for i in range(len(csv_list)):
    df_list.append(pd.read_csv(f'data/pricefetch/{csv_list[i]}'))

master_df = pd.concat(df_list) 

