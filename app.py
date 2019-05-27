import numpy as np
from flask import Flask, request, render_template
import pandas as pd
import joblib
import altair as alt
import glue

app = Flask(__name__)

releases = ['test1', 'test2', 'test3', 'test4']

@app.route('/', methods=['GET', 'POST'])
def index():
    stored_number = 1
    if request.method == 'POST':
        stored_number += 1

    # NOTE note: just slap a .serve() on the end of an altair chart to have it open up in another window

   # pass in the dictionary containing info here, eg. game=game from bot_paper_scissors        
    return render_template('index.html', stored_number=stored_number, releases=releases) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


