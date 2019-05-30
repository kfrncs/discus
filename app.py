#!/usr/bin/python
import numpy as np
from flask import Flask, request, render_template
from fbprophet import Prophet
import pandas as pd
import joblib
import altair as alt
import glue
from glue import df_discogs, df_popsike
import requests
from bs4 import BeautifulSoup
import re
from market_scrape import market_scrape
import pprint

# my prophet.py, not fbprophet
from prophet import log_transform, inverse_log_transform, prophesy

app = Flask(__name__)

releases = list(df_popsike['release_id'].unique())

@app.route('/', methods=['GET', 'POST'])
def index():
    chosen_release = None
    current_market = {}
    if request.method == 'POST':
        chosen_release = int(request.form['release_dropdown'])
        df_current = df_popsike[df_popsike['release_id'] == chosen_release].copy()

        ### prophet
        df_future = prophesy(df_current)

        current_market = market_scrape(chosen_release)
        for i in range(len(current_market)):
            print(current_market[i])
            print()
        ### visualization

        # later desired behaviour (see chart.py)
        # make_chart(df_current)

        # make chart (TODO: refactor behaviour to fit chart.py)
        base = alt.Chart(df_current.reset_index(),
                width=1150,
                height=450).encode(x='year(year):O').properties(
            title= df_current['title'].iloc[0] + ' - ' +  df_current['artist'].iloc[0]
        )
        
        future = alt.Chart(df_future.reset_index(), width=650).encode(x='year(year):O').properties()

        alt.layer(
                base.mark_line(color='red').encode(y='min:Q', tooltip='min:Q'),
                base.mark_line(color='blue').encode(y='avg:Q', tooltip='avg:Q'),
                base.mark_line(color='green').encode(y='max:Q', tooltip='max:Q'),
                future.mark_line(color='red').encode(y='min:Q'),
                future.mark_line(color='blue').encode(y='avg:Q'),
                future.mark_line(color='green').encode(y='max:Q')
        ).interactive().serve()
        # you'll need this for prophet viz:
        # mark_line(strokeDash=[1,1])

    return render_template('index.html', releases=releases, df_popsike=df_popsike, chosen_release=chosen_release,
            current_market=current_market) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
