from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re,os, sys

DATA_PATH = os.path.dirname(os.path.realpath(__file__))+ '/data/virus_world.csv' 
COUNTRIES = ['China', 'Italy','USA','Spain','Germany','France','S. Korea','UK','Total:']
HEADER = False


""" STEP 1. SCRAPE TABLE FROM URL """
url = 'https://www.worldometers.info/coronavirus/'
response = requests.get(url)
page = response.text
soup = BeautifulSoup(page,"html5lib")
tb = soup.find("table", {"id": "main_table_countries_yesterday"})


#print (tb)
""" STEP 2. CONVERT TO DATAFRAME """
tb = re.sub(r'<.*?>', lambda g: g.group(0).upper(), str(tb))
df = pd.read_html(str(tb))[0]
df = df[['Country,Other', 'TotalCases', 'TotalDeaths', 'TotalRecovered', 'Tot Cases/1M pop']]
df = df.loc[df['Country,Other'].isin(COUNTRIES)]
df['date'] = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
#
#
if os.path.exists(DATA_PATH):
	do = pd.read_csv(DATA_PATH,index_col=0)
	if do.iloc[-1]['TotalCases'] == df.iloc[-1]['TotalCases']:
		print ('Already update-to-date')
		sys.exit()
else:
	do = pd.DataFrame()
	

pd.concat([do,df]).to_csv(DATA_PATH)


print ('Update successfully !')