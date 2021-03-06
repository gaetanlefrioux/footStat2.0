import numpy as np

''' Mother class for all the models '''
''' All the models should implements those methods '''
class Model:
    def __init__(self):
        pass
    def computeMatchesProbas(self, data):
        pass

    def getTeams(self, data):
        team = set()
        for i in range(data.size):
            team.add(data[i]["HomeTeam"])
            team.add(data[i]["AwayTeam"])
        return team

    def orderDataByDate(self, data):
        return np.sort(data, axis=0, order="Date")
