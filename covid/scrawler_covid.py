from bs4 import BeautifulSoup
from ast import literal_eval
import requests
import re, json
import pandas as pd

def get_text_bs(soup):
	v = {}
	process_array = lambda x : literal_eval(x.split(':')[1].replace(' ',''))

	for chart in soup.select("script"):
		if 'Highcharts.chart' in str(chart):
			chart = str(chart).replace('\n','').split('       ')
			for sector in chart:
				if 'categories' in sector and 'date' not in v.keys():
					v['date'] = process_array(sector)
				if 'text' in sector:
					title = sector
				if 'data' in sector:
					if 'Total Coronavirus Cases' in title:
						v['total'] = process_array(sector)
					elif 'Total Coronavirus Deaths' in title:
						v['death'] = process_array(sector)
					elif 'Currently Infected' in title:
						v['active'] = process_array(sector)
					else:
						continue
	df = pd.DataFrame(v)
	df['date'] = pd.to_datetime(df['date'],format='%b%d,%Y')
	df.set_index('date', drop=True,inplace=True)
	return df


def get_world_data():
	""""
	COVID-19 WORLD DATA
	"""
	
	url = "https://www.worldometers.info/coronavirus/"
	response = requests.get(url)
	page = response.text
	body = BeautifulSoup(page,"html5lib").body
	if body is None:
		return None
	
	df = get_text_bs(body)
	df.to_csv('data/covid_world.csv')
	print ('-------- covid_world.csv is ready in the data folder ------- ')


	
def data_by_country(countries):
	""""
	COVID-19 WORLD DATA
	"""
	rs = []
	if isinstance(countries,str):
		countries = [countries]
		
	for country in countries:
		url = "https://www.worldometers.info/coronavirus/country/" + country
		response = requests.get(url)
		page = response.text
		soup = BeautifulSoup(page,"html5lib")
		
		rs.append(get_text_bs(soup).add_suffix('_'+country))
	df = pd.concat(rs,axis=1)
	df.to_csv('data/covid_countries.csv')
	print ('-------- covid_countries.csv is ready in the data folder ------- ')

	
	
"""add to COUNTRY if you want to include more,
   find country code on the worldmeters website
"""



COUNTRY = ['us','china','italy','spain','south-korea']	
#get_world_data()
data_by_country(countries=['china','us'])

