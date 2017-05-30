from flask import Flask, render_template, request, redirect
import requests
from bokeh.plotting import figure,output_file,save
from bokeh.embed import components
import pandas as pd

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
#  return redirect('/index')
  return redirect('/stock')
  
@app.route('/stock',methods = ['GET', 'POST'])
def stock():
	if request.method == 'GET':
		return render_template('stock.html')
	else:
		app.vars['stock'] = request.form['ticker']
		app.vars['price_type'] = request.form['price_type']
		price_type = dict(Closing = 'Close',
						  Adjusted_closing = 'Adj. Close',
						  Opening = 'Open',
						  Adjusted_opening = 'Adj. Open')
		# download data
		api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % app.vars['stock']
		session = requests.Session()
		session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
		raw_data = session.get(api_url)
		# manage data
		content = raw_data.json()
		col_names = content.get('column_names')
		data = content.get('data')
		df = pd.DataFrame(data, columns = col_names).set_index('Date')
		df.index = pd.to_datetime(df.index) # convert index to datetime

		# plot
		output_file("./templates/plot.html")	
		plot = figure(#tools=TOOLS,
					  title='Data from Quandle WIKI set: %s' % app.vars['stock'] ,
					  x_axis_label='date',
					  x_axis_type='datetime')
		script, div = components(plot)
		plot.line(df.index, df[price_type[app.vars['price_type']]], legend = app.vars['stock'])
		save(plot)
		
		return render_template('plot.html', script=script, div=div)
		#return app.vars['price_type']



if __name__ == '__main__':
  app.run(port=33507) #, debug = True)

