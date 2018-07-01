import data_loader as dl
import models.poisson_model as pm

loader = dl.DataLoader()
poissonModel = pm.PoissonModel(15, 5)
data = loader.loadFiles(['france1'])
poissonModel.computeMatchesProbas(data)
