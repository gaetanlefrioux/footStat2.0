import data_loader as dl

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

''' check all the consistency criterias for each competition and seasons '''
def get_consistency_summary(loader):
	fails = []
	for competition in loader.availableCompetitions:
		for season in loader.getAvailableSeasons(competition):
			filename = competition+"/"+season
			data = loader.load(competition, season, 'all')
			nmatch_consistency = check_nmatch_consistency(data)
			if nmatch_consistency == False:
				print('Debug pour le fichier %s/%s\n'%(competition, season))
				nmatch_consistency = check_nmatch_consistency(data, True)
				fails.append([
					filename,
				])
	return fails
