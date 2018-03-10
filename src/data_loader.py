import numpy as np
import sys
import os

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
			return None
		else:
			return os.listdir(self.directory+competition)

	def load(self, competition, season, colums=[0, 9]):
		if colums == 'all':
			usecols = None
		else:
			usecols = np.arange(colums[0], colums[1])
		try:
			data = np.genfromtxt(
				self.directory+competition+"/"+season, 
				delimiter=self.delimiter, 
				names=True,
				dtype=None,
				missing_values=np.nan,
				usecols=usecols
			)
			return data
		except:
			e = sys.exc_info()
			print "error while loading season %s of competition %s : \n %s" % (season, competition, e)
