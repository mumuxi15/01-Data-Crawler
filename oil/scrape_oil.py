from bs4 import BeautifulSoup
from ast import literal_eval
import requests
import re, json
import pandas as pd
import sqlite3

def get_text_bs(tree):
	""" extract data array from the charts 
		input: html
		output: dict
	"""
	body = tree.body
	if body is None:
		return None
	v = {}
	data = []
	tb = body.select('table')[0]
	for tr in tb.find_all('tr')[1::]:
		product = tr.get('data-spreadsheet')
		for td in tr.find_all('td'):
			if td.get('data-price'):
				price = td.get('data-price')
			if td.get('data-stamp'):
				timestamp = td.get('data-stamp')	
		data.append([product,price,timestamp])
	return data

def get_oil_price(url,engine):
	r = {}
	response = requests.get(url)
	page = response.text
	soup = BeautifulSoup(page,"html5lib")
		
	data = get_text_bs(soup)
	df = pd.DataFrame(data,columns=['product_name','price','timestamp'])
	df.to_sql('oil',con=engine,if_exists='append')
	
