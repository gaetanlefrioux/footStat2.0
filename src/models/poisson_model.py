import model as model
import numpy as np
import math as math

''' Class implementing the poissonModel '''
class PoissonModel(model.Model):

    def __init__(self, globalRange, teamRange, maxGoal):
        self.globalRange = globalRange
        self.teamRange = teamRange
        self.maxGoal = maxGoal
        self.events = ['score', 'winner', '+/-2.5']

    def getProbas(self, param):
        probas = []
        for i in range(self.maxGoal):
            probas.append((math.pow(param, i)/math.factorial(i))*math.exp(-param))
        return probas

    def computeMatchesProbas(self, data):
        data = self.orderDataByDate(data)
        self.eventResults = np.ones([data.size, len(self.events)])
        for m in range(data.size):
            #print(data[m]["Date"].strftime('%m/%d/%Y')+" "+data[m]['HomeTeam']+" "+data[m]['AwayTeam'])
            awayTeam = data[m]['AwayTeam']
            homeTeam = data[m]['HomeTeam']
            # away Team Defense
            currentAwayTeamConceded = float(0)
            # count matches away Team
            nbMatchCurrentAwayTeam = float(0)
            # away Team Attack
            currentAwayTeamScored = float(0)
            # home team defense
            currentHomeTeamConceded = float(0)
            # count matches home Team
            nbMatchCurrentHomeTeam = float(0)
            # home team Attack
            currentHomeTeamScored = float(0)
            # global attack
            globalScoredAtHome = float(0)
            globalScoredAtAway = float(0)
            # global defense
            globalConcededAtHome = float(0)
            globalConcededAtAway = float(0)
            # global match count
            nbMatchGlobal = float(0)
            j = m - 1
            done = False
            while j >= 0 and not done:
                # Update global
                if nbMatchGlobal < self.globalRange:
                    # Update global attack
                    globalScoredAtHome += data[j]['FTHG']
                    globalScoredAtAway += data[j]['FTAG']
                    # Update global defense
                    globalConcededAtHome += data[j]['FTAG']
                    globalConcededAtAway += data[j]['FTHG']
                    nbMatchGlobal += 1
                #Update away team at Away
                if data[j]["AwayTeam"] == awayTeam and nbMatchCurrentAwayTeam < self.teamRange:
                    currentAwayTeamConceded += data[j]["FTHG"]
                    currentAwayTeamScored += data[j]["FTAG"]
                    nbMatchCurrentAwayTeam += 1
                #Update home team at Home
                if data[j]["HomeTeam"] == homeTeam and nbMatchCurrentHomeTeam < self.teamRange:
                    currentHomeTeamConceded += data[j]["FTAG"]
                    currentHomeTeamScored += data[j]["FTHG"]
                    nbMatchCurrentHomeTeam += 1
                done = nbMatchGlobal >= self.globalRange and nbMatchCurrentAwayTeam >= self.teamRange
                done = done and nbMatchCurrentHomeTeam >= self.teamRange
                j -= 1
            # Not enough data to extrapolate the results
            if not done:
                for e in range(len(self.events)):
                    self.eventResults[m][e] = 1
            # Try to guess events results
            else:
                # compute home team attack strength at home
                homeTeamAttack = (currentHomeTeamScored/nbMatchCurrentHomeTeam)/(globalScoredAtHome/nbMatchGlobal)
                # compute home team defense strength at home
                homeTeamDefense = (currentHomeTeamConceded/nbMatchCurrentHomeTeam)/(globalConcededAtHome/nbMatchGlobal)
                # compute away team attack strength at away
                awayTeamAttack = (currentAwayTeamScored/nbMatchCurrentAwayTeam)/(globalScoredAtAway/nbMatchGlobal)
                # compute away team defense strength at away
                awayTeamDefense = (currentAwayTeamConceded/nbMatchCurrentAwayTeam)/(globalConcededAtAway/nbMatchGlobal)

                goalHomeTeam = homeTeamAttack*awayTeamDefense*(globalScoredAtHome/nbMatchGlobal)
                goalAwayTeam = awayTeamAttack*homeTeamDefense*(globalScoredAtAway/nbMatchGlobal)

                homeGoalProbas = self.getProbas(goalHomeTeam)
                awayGoalProbas = self.getProbas(goalAwayTeam)
                score = [];
                maxScoreProbas = -float("inf")
                homeWinProbas = 0;
                awayWinProbas = 0;
                equalityProbas = 0;
                more25Probas = 0;
                less25Probas = 0;
                for k in range(self.maxGoal):
                    for x in range(self.maxGoal):
                        proba = homeGoalProbas[k]*awayGoalProbas[x]
                        if proba > maxScoreProbas:
                            maxScoreProbas = proba
                            score = [k, x]
                        if k > x:
                            homeWinProbas += proba
                        elif k == x:
                            equalityProbas += proba
                        else:
                            awayWinProbas += proba
                        if k+x > 2.5:
                            more25Probas += proba
                        else:
                            less25Probas += proba
                if score[0] == data[m]["FTHG"] and score[1] == data[m]["FTAG"]:
                    self.eventResults[m][0] = 2
                else:
                    self.eventResults[m][0] = 0
                if homeWinProbas > awayWinProbas and homeWinProbas > equalityProbas:
                    if data[m]["FTHG"] > data[m]["FTAG"]:
                        self.eventResults[m][1] = 2
                    else:
                        self.eventResults[m][1] = 0
                elif awayWinProbas > homeWinProbas and awayWinProbas > equalityProbas:
                    if data[m]["FTHG"] < data[m]["FTAG"]:
                        self.eventResults[m][1] = 2
                    else:
                        self.eventResults[m][1] = 0
                elif equalityProbas > awayWinProbas and equalityProbas > homeWinProbas:
                    if data[m]["FTHG"] == data[m]["FTAG"]:
                        self.eventResults[m][1] = 2
                    else:
                        self.eventResults[m][1] = 0
                else:
                    self.eventResults[m][1] = 1
                if more25Probas > less25Probas:
                    if data[m]["FTHG"] + data[m]["FTAG"] > 2.5:
                        self.eventResults[m][2] = 2
                    else:
                        self.eventResults[m][2] = 0
                elif less25Probas > more25Probas:
                    if data[m]["FTHG"] + data[m]["FTAG"] < 2.5:
                        self.eventResults[m][2] = 2
                    else:
                        self.eventResults[m][2] = 0
                else:
                    self.eventResults[m][2] = 1
        return self.eventResults
