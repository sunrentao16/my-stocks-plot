from flask import Flask, render_template, request, redirect
import requests
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import pandas as pd
from datetime import datetime


stock = 'GOOG'
api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
raw_data = session.get(api_url)

content = raw_data.json()

col_names = content.get('column_names')
data = content.get('data')
print col_names


df = pd.DataFrame(data, columns = col_names).set_index('Date')
df.index = pd.to_datetime(df.index)

print type(df.index)
print df.index

#--------------------------------
output_file("./templates/plot_1.html")	
plot = figure(#tools=TOOLS,
			  title='Data from Quandle WIKI set',
			  x_axis_label='date',
			  x_axis_type='datetime')
script, div = components(plot)
plot.line(df.index, df.Open, legend = 'stock')

show(plot)

#return render_template('index.html', script=script, div=div)


