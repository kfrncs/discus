#!/usr/bin/python
import numpy as np
from flask import Flask, request, render_template
from fbprophet import Prophet
import pandas as pd
import joblib
import altair as alt
import glue
from glue import df_discogs, df_popsike

# my prophet.py, not fbprophet
from prophet import log_transform, inverse_log_transform, prophesy

app = Flask(__name__)

releases = list(df_popsike['release_id'].unique())

@app.route('/', methods=['GET', 'POST'])
def index():
    chosen_release = None
    if request.method == 'POST':
        chosen_release = int(request.form['release_dropdown'])
        df_current = df_popsike[df_popsike['release_id'] == chosen_release].copy()

        ### prophet
        # df_future = prophesy(df_current)



        ### visualization

        # later desired behaviour (see chart.py)
        # make_chart(df_current)

        # make chart (TODO: refactor behaviour to fit chart.py)
        base = alt.Chart(df_current.reset_index(),
                width=1150,
                height=450).encode(x='year(year):O').properties(
            title= df_current['title'].iloc[0] + ' - ' +  df_current['artist'].iloc[0]
        )

        # this is where prophet predictions will go, looking like ^^^

        alt.layer(
                base.mark_line(color='red').encode(y='min:Q', tooltip='min:Q'),
                base.mark_line(color='blue').encode(y='avg:Q', tooltip='avg:Q'),
                base.mark_line(color='green').encode(y='max:Q', tooltip='max:Q')
        ).interactive().serve()
        # you'll need this for prophet viz:
        # mark_line(strokeDash=[1,1])

    return render_template('index.html', releases=releases, df_popsike=df_popsike, chosen_release=chosen_release) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
