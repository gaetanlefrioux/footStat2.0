import data_loader as dl
import numpy as np
''' Check datas consistency '''

loader = dl.DataLoader()

''' check if a file has the number of match expected '''
def check_nmatch_consistency(data, debug=False):
	team = set()
	for i in range(data.size):
		team.add(data[i]["HomeTeam"])
	theorical_nmatch = len(team)*(len(team) - 1)
	if debug:
		print("Teams\n")
		print(team)
		print("\n")
		print("Theorical number of match : %d\n" % theorical_nmatch)
		print("Real number of match : %d\n" % data.size)
	return theorical_nmatch == data.size

''' check match number criterias for each competition and seasons '''
def get_nmatch_summary(loader):
	fails = []
	for competition in loader.availableCompetitions:
		for season in loader.getAvailableSeasons(competition):
			filename = competition+"/"+season
			data = loader.load(competition, season)
			nmatch_consistency = check_nmatch_consistency(data)
			if nmatch_consistency == False:
				print('Debug pour le fichier %s/%s\n'%(competition, season))
				nmatch_consistency = check_nmatch_consistency(data, True)
				fails.append([
					filename,
				])
	return fails

''' check date validity and date order for a file '''
''' we need the file name to check if year is valid '''
def check_date_consistency(data, filename):
	if str(data[0]["Date"].year) not in filename:
		#print('Error in 1st line of file %s' % filename)
		return False
	for i in range(1, data.size):
		if str(data[i]["Date"].year) not in filename:
			#print('Error in line %d of file %s False year' % (i, filename))
			return False
		if data[i-1]["Date"] > data[i]["Date"]:
			#print('Error in line %d of file %s False day' % (i, filename))
			return False
	return True

''' check date order criterias for each competition and seasons '''
def get_date_summary(loader):
	fails = []
	for competition in loader.availableCompetitions:
		for season in loader.getAvailableSeasons(competition):
			filename = competition+"/"+season
			data = loader.load(competition, season)
			date_consistency = check_date_consistency(data, filename)
			if date_consistency == False:
				fails.append(filename)
	return fails

''' Get the commons complete attributes from files '''
def getCommonAttributes(competition, years=False):
	attributes = {}
	if years == False:
		years = loader.getAvailableSeasons(competition)
	for y in years:
		data = loader.load(competition, y)
		for att in data.dtype.names:
			isComplete = True
			i = 0
			while i < data.size and isComplete:
				isComplete = data[i][att] != np.nan
				i += 1
			if att not in attributes.keys():
				attributes[att] = []
			attributes[att] += [isComplete]
	commonAttributes = []
	for att in attributes.keys():
		if len(attributes[att]) == len(years):
			ok = True
			for b in attributes[att]:
				ok = ok and b
				if ok == False:
					break
			if ok == True:
				commonAttributes += [att]
	return commonAttributes


''' 2017-2018 files will fail the number of matches check since the season isn't ended yet '''
#print(get_date_summary(loader))
#print(get_nmatch_summary(loader))
