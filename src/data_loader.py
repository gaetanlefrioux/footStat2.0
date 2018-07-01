import numpy as np
import sys
import os
from datetime import datetime

''' Class for loading and cleaning datas '''
class DataLoader:

	def __init__(self):
		self.directory = "../data/"
		self.availableCompetitions = self.getAvailableCompetitions()
		self.delimiter = ','

	def getAvailableCompetitions(self):
		return os.listdir(self.directory)

	def getAvailableSeasons(self, competition):
		if(competition not in self.availableCompetitions):
			raise Exception("The competition %s is not available" % competition)
			sys.exit()
		else:
			return os.listdir(self.directory+competition)

	def load(self, competition, season, colums='all', dtype=None):
		if colums == 'all':
			usecols = None
		else:
			usecols = colums
		try:
			data = np.genfromtxt(
				self.directory+competition+"/"+season,
				delimiter=self.delimiter,
				names=True,
				dtype=dtype,
				missing_values=np.nan,
				usecols=usecols,
				converters = {"Date": self.parseDate},
				encoding = 'utf-8'
			)
			return data
		except Exception as e:
			print("error while loading season "+season+" of competition "+competition+" : \n "+e)

	# Load and concatenate all the competitions and seasons given
	def loadFiles(self, competitions, seasons='all', columns=range(9)):
		data = None
		for c in competitions:
			# If no seasons are given we take all of the seasons available
			if seasons == 'all':
				seasons = self.getAvailableSeasons(c)
			for s in seasons:
				if data is not None:
					seasonData = self.load(c, s, columns, np.dtype(data.dtype))
					data = np.concatenate((data, seasonData), axis=0)
				else:
					data = self.load(c, s, columns)
		return data

	def loadStandAloneFile(self, path):
		try:
			data = np.genfromtxt(
				path,
				delimiter=self.delimiter,
				names=True,
				dtype=None,
				missing_values=np.nan,
				usecols=None,
				converters = {"Date": self.parseDate},
				encoding = 'utf-8'
			)
			return data
		except Exception as e:
			print("error while loading file "+path+" : \n "+e)

	def parseDate(self, d):
		try:
			if(len(d) == 8):
				return datetime.strptime(d, '%d/%m/%y')
			elif(len(d) == 10):
				return datetime.strptime(d, '%d/%m/%Y')
		except Exception as e:
			print("Error while parsing date: %s" %e)

	def write(self, path, data):
		np.savetxt(
			path,
			data,
			delimiter=",",
			header=','.join(data.dtype.names),
			comments='',
			encoding="utf-8",
			fmt='%s'
		)
