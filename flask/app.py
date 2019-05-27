import numpy as np
from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    stored_number = 1
    if request.method == 'POST':
        stored_number += 1

   # pass in the dictionary containing info here, eg. game=game from bot_paper_scissors        
    return render_template('index.html', stored_number=stored_number) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


