import pandas as pd
import sqlite3

engine = sqlite3.connect('data/collection.db')
url = {'oil':'https://oilprice.com/oil-price-charts'}