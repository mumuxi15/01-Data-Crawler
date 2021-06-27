from scipy.optimize import curve_fit
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import time
 
def logistic_function(t, K, P0, r):
	exp = np.exp(-r * t)
	return 1 / (K + (exp+1) * P0)
 
def predict(c):
	
	predict_days = 20
	data = pd.read_json('data/virus_world.json')[c]
	confirm = np.array(data['total'])
	scaler = np.max(confirm)
	confirm = confirm/(scaler)


	x = np.arange(len(confirm))
	# curve fit
	popt, pcov = curve_fit(logistic_function, x, confirm,maxfev=2000)
	#predit future
	predict_x = list(x) + [x[-1] + i for i in range(1, 1 + predict_days)]
	predict_x = np.array(predict_x)
	predict_y = logistic_function(predict_x, popt[0], popt[1], popt[2])
	plt.figure(figsize=(15, 8))
	plt.plot(x, confirm, 's',label="confimed infected number")
	plt.plot(predict_x, predict_y, '--',label="predicted infected number")
	plt.xticks(rotation=90)
	plt.yticks(rotation=90)
 	
	plt.suptitle("Coronavirus cases prediction in %s for the next %d days (Pred = %d,  r=%.2f)"%(c.capitalize(),predict_days,scaler*predict_y[-1], popt[2]), fontsize=12, fontweight="bold")
	plt.title("Predict time:{}".format(time.strftime("%Y-%m-%d", time.localtime())), fontsize=16)
	plt.xlabel('date', fontsize=14)
	plt.ylabel('infected number', fontsize=14)
	plt.show()
 
predict(c='china')