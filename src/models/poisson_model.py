import model as model
import numpy as np

''' Class implementing the poissonModel '''
class PoissonModel(model.Model):

    def __init__(self, range):
        self.range = range
        self.events = ['winner', '+2.5']

    def computeMatchesProbas(self, data):
        data = self.orderDataByDate(data)
        self.eventResults = np.zeros([data.size, len(self.events)])
        for i in range(data.size):
            awayTeam = data[i]['AwayTeam']
            homeTeam = data[i]['HomeTeam']
            # away Team Defense
            currentAwayTeamConcededAtHome = 0
            nbMatchCurrentAwayTeamConcededAtHome = 0
            currentAwayTeamConcededAtAway = 0
            nbMatchCurrentAwayTeamConcededAtAway = 0
            # away Team Attack
            currentAwayTeamScoredAtHome = 0
            nbMatchCurrentAwayTeamScoredAtHome = 0
            currentAwayTeamScoredAtAway = 0
            nbMatchCurrentAwayTeamScoredAtAway = 0
            # home team defense
            currentHomeTeamConcededAtHome = 0
            nbMatchCurrentHomeTeamConcededAtHome = 0
            currentHomeTeamConcededAtAway = 0
            nbMatchCurrentHomeTeamConcededAtAway = 0
            # home team Attack
            currentHomeTeamScoredAtHome = 0
            nbMatchCurrentHomeTeamScoredAtHome = 0
            currentHomeTeamScoredAtAway = 0
            nbMatchCurrentHomeTeamScoredAtAway = 0
            # global attack
            globalScoredAtHome = 0
            globalScoredAtAway = 0
            # global defense
            globalConcededAtHome = 0
            globalConcededAtAway = 0
            # global match count
            nbMatchGlobal = 0
            j = i - 1
            done = False
            while j >= 0 and not done:
                # Update global
                if nbMatchGlobal < self.range:
                    # Update global attack
                    globalScoredAtHome += data[j]['FTHG']
                    globalScoredAtAway += data[j]['FTAG']
                    # Update global defense
                    globalScoredAtHome += data[j]['FTHG']
                    globalScoredAtAway += data[j]['FTAG']
                    nbMatchGlobal += 1
