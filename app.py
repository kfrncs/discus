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
    stored_number = 1
    if request.method == 'POST':
        stored_number += 1

    # NOTE note: just slap a .serve() on the end of an altair chart to have it open up in another window

   # pass in the dictionary containing info here, eg. game=game from bot_paper_scissors        
    return render_template('index.html', stored_number=stored_number, releases=releases, df_popsike=df_popsike) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


