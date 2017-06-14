from flask import Flask, render_template, request, redirect
import pandas as pd
import requests as req
import simplejson as json
from bokeh.plotting import Figure
from bokeh.embed import components

app = Flask(__name__)

def get_data(requested_ticker):

    #requested_ticker = "FB"
    search_params = {"ticker": requested_ticker, 
            "qopts.export": "date,open", 
            "api_key": "96MxM7FkumHEe4shswrC"}

    dtf = req.get(url = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", 
            params = search_params)

    col_names = [d['name'] for d in dtf.json()['datatable']['columns']]
    col_dates = [row[col_names.index('date')] for row in dtf.json()['datatable']['data']]

    col_values = list()
    for col_to_pull in col_names:
        col_values.append([row[col_names.index(col_to_pull)] for row in dtf.json()['datatable']['data']])
    
    col_dates = pd.to_datetime(col_dates)

    return(col_names, col_values, col_dates)


def make_plot(col_names, col_values, col_dates, cols):
    plot = Figure(
            title = 'Data from Quandl WIKI set', 
            x_axis_label = 'date',
            x_axis_type = 'datetime')

    colors = ['#4286f4', '#f44242', '#f4bc42', '#50f442', '#42f4e5']

    for color, col in zip(range(4), cols): 
        plot.line(col_dates, 
                col_values[col_names.index(col)], 
                color = colors[color])

    return(plot)

app.ticker = "" 

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods = ['GET', 'POST'])
def index():
    #return render_template('index.html')
#    app.ticker = request.form.get('ticker')
    return render_template('index.html')#, ticker = app.ticker)
  

@app.route('/graph', methods = ['GET', 'POST'])
def graph():

    #names of available checkboxes
    cols_to_check = ['open', 'high', 'low', 'close', 'volume']

    #get values for those boxes
    cols_to_pull = []
    for col in cols_to_check: 
        if request.args.get(col):
            cols_to_pull.append(col)
        else: 
            pass
    
    col_names, col_values, col_dates = get_data(request.args.get('ticker'))

    plot = make_plot(col_names, col_values, col_dates, cols_to_pull)
    script, div = components(plot)

    return render_template('graph.html', 
            script = script, 
            div = div, 
            xaxis = cols_to_pull)

if __name__ == '__main__':
  app.run(port=33507, debug = True)
