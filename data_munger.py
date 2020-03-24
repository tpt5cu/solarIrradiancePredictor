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
#Get Cloud Data
def getDarkSkyCloudCoverForYear(year, lat, lon, key, units='si'):
	cloudCoverByHour = {}
	coords = '%0.2f,%0.2f' % (lat, lon)
	times = list(pd.date_range('{}-01-01'.format(year), '{}-12-31'.format(year), freq='D'))
	while times:
		time = times.pop(0)
		print(time)
		url = 'https://api.darksky.net/forecast/%s/%s,%s?exclude=daily,alerts,minutely,currently&units=%s' % (key, coords, time.isoformat(), units ) 
		res = requests.get(url).json()
		try:
			dayData = res['hourly']['data']
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

def writeCloudsToCsv(year, cloudsForTheYear, filepath):
#See the results in a .csv
	filename = filepath.strip('.csv') + '_cloud_output_darksky_'
	w = csv.writer(open(filename+str(year)+".csv", "w"))
	for key, val in cloudsForTheYear.items():
		w.writerow([key, val])
	return

#Fix below
# def readCloudCoverData(year):
# #in case you dont have cloudsForTheYear defined, run this to get data from the saved .csv
# 	#import csv
# 	timelist = []
# 	cloudslist = []
# 	with open("cloud_output_darksky_"+year+".csv", newline='') as infile:
# 	    reader = csv.reader(infile, delimiter=',')
# 	    for row in reader:
# 	        timelist.append(int(row[0]))
# 	        cloudslist.append(float(row[1]))

# 	cloudsForTheYear = dict(zip(timelist, cloudslist))
# 	print(cloudsForTheYear)
# 	return cloudsForTheYear




def makeDb(cloudsForTheYear, sourceData, targetFileName):
	#get 2015 nrsdb data
	df = pd.read_csv(sourceData, skiprows=2)
	#Create new DF
	print(df.iloc[0]['Year'])
	print(len(df))
	timestamps = []
	for i in range(len(df)):
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
	print(len(df['timestamps']))
	for i in df['timestamps']:
	    try:
	        print(i, cloudsForTheYear[i])
	        cloudCover.append(cloudsForTheYear[i])
	    except KeyError:
	        cloudCover.append(0.0)
	print(len(cloudCover))

	#Add into new DB
	df['Cloud Cover'] = pd.Series(cloudCover, index = df.index)
	df.to_csv(targetFileName, index=False)

	return df 

#Fix below
# def getCloudData(year):
# 	year=2015
# 	cloudsForTheYear = getDarkSkyCloudCoverForYear(year, 43.85, -99.5, key)
# 	writeCloudsToCsv(year, cloudsForTheYear)
# 	return cloudsForTheYear


def readFromDiskAndMakeDf(year):
	cloudsForTheYear = readCloudCoverData(year)
	df=makeDb(cloudsForTheYear)
	return df

def pipeline(lat, lon, year, sourceDataName, targetDataFileName):
	_key = '31dac4830187f562147a946529516a8d'
	_cwd = os.getcwd()
	_Raw_Data = os.path.join(_cwd, 'Raw_Data')
	_Testing_Data = os.path.join(_cwd, 'Testing_Data')
	cloudsForTheYear = getDarkSkyCloudCoverForYear(year, lat, lon, _key, units='si')
	writeCloudsToCsv(year, cloudsForTheYear, os.path.join(_Testing_Data, targetDataFileName))
	df = makeDb(cloudsForTheYear, os.path.join(_Raw_Data, sourceDataName), os.path.join(_Testing_Data, targetDataFileName))
	print("db finished!")


if __name__ == "__main__":
	year = 2018
	# pipeline(,, year, 'RAW_psm_VA_Charlottesville'+str(year)+'.csv', 'Charlottesville_psm_'+str(year)+'.csv')
	pipeline(30.581736, -98.024098, year, 'RAW_psm_TX_Austin'+str(year)+'.csv', 'Austin_psm_'+str(year)+'.csv')
	# cloudsForTheYear = getDarkSkyCloudCoverForYear(year, lat, lon, key, units='si')
	# writeCloudsToCsv(year, cloudsForTheYear)
	# df = makeDb(cloudsForTheYear, filename)
	# print("db finished!")

	



