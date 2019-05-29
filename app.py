#!/usr/bin/python
import numpy as np
from flask import Flask, request, render_template
import pandas as pd
import joblib
import altair as alt
import glue
from glue import df_discogs, df_popsike

app = Flask(__name__)

releases = list(df_popsike['release_id'].unique())

@app.route('/', methods=['GET', 'POST'])
def index():
    chosen_release = None
    if request.method == 'POST':
        chosen_release = int(request.form['release_dropdown'])
        df_current = df_popsike[df_popsike['release_id'] == chosen_release].copy()
        base = alt.Chart(df_current.reset_index(), width=1150).encode(x='year(year):O').properties(
            title= df_current['title'].iloc[0] + ' - ' +  df_current['artist'].iloc[0]
        )

        alt.layer(
                base.mark_line(color='red').encode(y='min:Q', tooltip='min:Q'),
                base.mark_line(color='blue').encode(y='avg:Q', tooltip='avg:Q'),
                base.mark_line(color='green').encode(y='max:Q', tooltip='max:Q')
        ).interactive().serve()

    return render_template('index.html', releases=releases, df_popsike=df_popsike, chosen_release=chosen_release) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
