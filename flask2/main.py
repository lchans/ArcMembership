"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template
app = Flask(__name__)
import csv

@app.route('/')
def generate_market_data():
	data = populate_data()
	params = populate_params()
	return render_template("index.html", data=data, params=params)

def populate_data(): 
	table = []
	with open('static/sampledata.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader: 
			table.append(row)
	return  table 

def populate_params(): 
	table = []
	with open ('static/sampleparams.txt', 'rb') as paramfile: 
		for line in paramfile: 
			table.append(line)
	print table
	return table
