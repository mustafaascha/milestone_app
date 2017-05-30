from flask import Flask, render_template, request, redirect
import pandas as pd
import requests as req
import simplejson as json
from bokeh.plotting import Figure
from bokeh.embed import components

app = Flask(__name__)

api =  "96MxM7FkumHEe4shswrC"
requested_ticker = "FB"
search_params = {"ticker": requested_ticker, 
        "qopts.export": "date,open", 
        "api_key": api}

dtf = req.get(url = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", 
        params = search_params)

open_price = []
for row in dtf.json()['datatable']['data']:
  open_price.append(row[2])

open_date = []
for row in dtf.json()['datatable']['data']:
  open_date.append(row[1])

open_date = pd.to_datetime(open_date)

def make_plot(open_date, open_price):
    plot = Figure(
            title = 'Data from Quandl WIKI set: FB for now', 
            x_axis_label = 'date',
            x_axis_type = 'datetime')

    plot.line(open_price, open_date)

    return(plot)


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  plot = make_plot(open_price, open_date)
  script, div = components(plot)
  return render_template('index.html', script = script, div = div)

if __name__ == '__main__':
  app.run(port=33507, debug = True)
