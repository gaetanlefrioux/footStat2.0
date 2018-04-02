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

	def load(self, competition, season, colums='all'):
		if colums == 'all':
			usecols = None
		else:
			usecols = colums
		try:
			data = np.genfromtxt(
				self.directory+competition+"/"+season, 
				delimiter=self.delimiter, 
				names=True,
				dtype=None,
				missing_values=np.nan,
				usecols=usecols,
				converters = {"Date": self.parseDate},
				encoding = 'utf-8'
			)
			return data
		except Exception as e:
			print "error while loading season %s of competition %s : \n %s" % (season, competition, e)

	def parseDate(self, d):
		try:
			if(len(d) == 8):
				return datetime.strptime(d, '%d/%m/%y')
			elif(len(d) == 10):
				return datetime.strptime(d, '%d/%m/%Y')	
		except Exception as e:
			print("Error while parsing date: %s" %e)
