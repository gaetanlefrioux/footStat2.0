import model as model

''' Class implementing the poissonModel '''
class PoissonModel(model.Model):

    def __init__(self, longRange, shortRange):
        self.longRange = longRange
        self.shortRange = shortRange
        self.events = ['winner']

    def computeMatchesProbas(self, data):
        print(self.getTeams(data))
