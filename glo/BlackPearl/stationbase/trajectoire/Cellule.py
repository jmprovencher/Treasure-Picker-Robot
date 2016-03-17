class Cellule():
    def __init__(self, x, y, atteignable):
        self.atteignable = atteignable
        self.x = x
        self.y = y
        self.parent = None
        self.poid = 0
        self.heuristique = 0
        self.priorite = 0
        self.distance = 0

    def getHeuristique(self, arriver):
        return 10 * (abs(self.x - arriver.x) + abs(self.y - arriver.y))

    def calculerDistance(self, arriver):
        self.distance = (arriver.x-self.x)**2+(arriver.y-self.y)**2
