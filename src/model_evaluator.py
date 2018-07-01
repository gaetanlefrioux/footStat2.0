import data_loader as dl
import numpy as np
import models.poisson_model as pm

loader = dl.DataLoader()
poissonModel = pm.PoissonModel(15, 15, 10)
for c in loader.getAvailableCompetitions():
    print(c+"\n")
    data = loader.loadFiles([c])
    results = poissonModel.computeMatchesProbas(data)
    resultSummary = np.zeros([len(poissonModel.events), 3])
    for i in range(data.size):
        for j in range(len(poissonModel.events)):
            if results[i][j] == float(2):
                resultSummary[j][0] += 1
            elif results[i][j] == float(0):
                resultSummary[j][1] += 1
            else:
                resultSummary[j][2] += 1
    for i in range(len(poissonModel.events)):
        betted = resultSummary[i][0] + resultSummary[i][1]
        win = (resultSummary[i][0]/betted)*100
        lost = (resultSummary[i][1]/betted)*100
        dontKnow = (resultSummary[i][2]/data.size)*100
        print(poissonModel.events[i]+": "+str(win)+" "+str(lost)+" "+str(dontKnow)+" "+"\n")
    print("\n")
