# discus
Projecting future record prices with FBProphet, visualization with Altair.

`my_token.py` contains a template to place your [Discogs](https://www.discogs.com/my) token, your wantlist (download from Discogs) and your [Popsike](https://www.popsike.com/) username and password.

`discus.py` scrapes current recommend sale prices from Discogs. This data was not sufficient for the model and was not used.

`popsike_scraper.py` uses Selenium to pull min / avg / max historical prices for each record from Popsike.

`glue.py` performs some cleaning functions on the data, also contains the DataFrames.

`market_scrape.py` pulls current data from the Discogs marketplace (i.e. records to buy)

`prophet.py` contains the bulk of the modelling with FBProphet. 

```app.py``` launches the local flask server, then navigate to `http://0.0.0.0:5000/` in your browser. Click a record from the dropdown list to 

`chart.py` contains not-yet-implemented prettier charts, and `EDA.ipynb` and `prophet_start.ipynb` were used for Exploratory Data Analysis and prototyping.