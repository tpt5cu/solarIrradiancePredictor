#!/usr/bin/env python
# coding: utf-8
#GENERAL DATA MUNGING SCRIPT
#FOR DARKSKY SKY DATA - TRAININD_DF FOR PANDAS


#STEP 1, GET DARK SKY DATA, put in dictionary

import requests
import datetime
import os
import pandas as pd
import csv

"""Darksky time machine request
https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]
key: 31dac4830187f562147a946529516a8d

params: year,lat,lon,
returns: cloud cover percentage

"""
#Exclude minutely, currently, daily, alerts
key='31dac4830187f562147a946529516a8d'
#Get Cloud Data
def getDarkSkyCloudCoverForYear(year, lat, lon, key, units='si'):
	cloudCoverByHour = {}
	coords = '%0.2f,%0.2f' % (lat, lon)
	times = list(pd.date_range('{}-01-01'.format(year), '{}-12-31'.format(year), freq='D'))
	while times:
		time = times.pop(0)
		url = 'https://api.darksky.net/forecast/%s/%s,%s?exclude=daily,alerts,minutely,currently&units=%s' % (key, coords, time.isoformat(), units ) 
		res = requests.get(url).json()
		try:
			dayData = res['hourly']['data']
			print(dayData)
		except KeyError:
			print("No day data!!!!!!")
			continue
		for hour in dayData:
			try:
				cloudCoverByHour[hour['time']] = hour['cloudCover']
			except KeyError:
				print("No Cloud Cover Data")
				pass
	return cloudCoverByHour

def writeCloudsToCsv(year, cloudsForTheYear, filename=None):
#See the results in a .csv
	if filename is None:
		filename = "darksky_"+str(year)+".csv"
	else:
		filename = filename.split(".csv")[0]
		filename = filename + 'cloud_output.csv'
	w = csv.writer(open(filename, "w"))
	for key, val in cloudsForTheYear.items():
	    w.writerow([key, val])
	return


def readCloudCoverData(year, filename=None):
#in case you dont have cloudsForTheYear defined, run this to get data from the saved .csv
	#import csv
	timelist = []
	cloudslist = []
	if filename is None:
		filename = "darksky_"+str(year)+".csv"
	else:
		filename = filename + 'cloud_output.csv'
	with open(filename, newline='') as infile:
	    reader = csv.reader(infile, delimiter=',')
	    for row in reader:
	        timelist.append(int(row[0]))
	        cloudslist.append(float(row[1]))

	cloudsForTheYear = dict(zip(timelist, cloudslist))
	print(cloudsForTheYear)
	return cloudsForTheYear




def makeDb(cloudsForTheYear, filename):
	#get 2015 nrsdb data
	df = pd.read_csv(filename, skiprows=2)
	#Create new DF
	print(df.iloc[0]['Year'])
	timestamps = []
	for i in range(2, len(df)):
	    year = (int(df.iloc[i]['Year']))
	    month = (int(df.iloc[i]['Month']))
	    day = (int(df.iloc[i]['Day']))
	    hour = (int(df.iloc[i]['Hour']))
	    date = datetime.datetime(year, month, day, hour)
	    timestamp = datetime.datetime.timestamp(date)
	    timestamps.append(timestamp)    
	df['timestamps'] = pd.Series(timestamps, index = df.index)
	# df['Cloud Cover'] = pd.Series(timestamps, index = df.index)
	# df['Cloud Cover'] = df['Cloud Cover'].astype(int)
	df['timestamps'] = df['timestamps'].astype(int)
	# df['Cloud Cover'] = pd.Series(np.random.randn(len(df['timestamps'])), index=df.index)
	print(df)
	#Create ordered list of all timestamps with a cloud cover, else add in a 0.0
	cloudCover = []
	#Read in cloud data from darksky, append with the timestamp. Else, 0.0
	for i in df['timestamps']:
	    try:
	        print(i, cloudsForTheYear[i])
	        cloudCover.append(cloudsForTheYear[i])
	    except KeyError:
	        cloudCover.append(0.0)
	print("Cloud Cover data length", len(cloudCover))
	assert len(cloudCover) == len(df['timestamps']), "Size of cloud data does not match db length!"

	#Add into new DB
	df['Cloud Cover'] = pd.Series(cloudCover, index = df.index)
	df.to_csv('psm_testing_data'+str(year)+'.csv', index=False)
	print(df)
	return df 


def getCloudData(year):
	cloudsForTheYear = getDarkSkyCloudCoverForYear(year, 43.85, -99.5, key)
	writeCloudsToCsv(year, cloudsForTheYear)
	return cloudsForTheYear


def readFromDiskAndMakeDf(year):
	cloudsForTheYear = readCloudCoverData(year)
	df=makeDb(cloudsForTheYear)
	return df

def pipeline(year, filename=None):
	dataPath = (os.path.dirname(os.path.dirname( __file__ )))
	if filename is None:
		filename =  ('psm_'+str(year)+'.csv')
	filename = os.path.join(dataPath, filename)
	print(filename)
	# cloudsForTheYear = getDarkSkyCloudCoverForYear(year, 43.85, -99.5, '31dac4830187f562147a946529516a8d', units='si')
	cloudsForTheYear = getDarkSkyCloudCoverForYear(year, 38.0086,-78.4532, '31dac4830187f562147a946529516a8d', units='si')
	print("******HERE ARE THE CLOUDS FOR THE YEAR*******")
	print(cloudsForTheYear)
	writeCloudsToCsv(year, cloudsForTheYear, filename)
	df = makeDb(cloudsForTheYear, filename)
	print("db finished!")



if __name__ == "__main__":
	pipeline(2018, 'psm_VA_Charlottesville2018.csv' )
	# cloudsForTheYear = getDarkSkyCloudCoverForYear(year, lat, lon, key, units='si')
	# writeCloudsToCsv(year, cloudsForTheYear)
	# df = makeDb(cloudsForTheYear, filename)
	# print("db finished!")