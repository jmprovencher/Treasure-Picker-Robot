##### REFACTORING STATUS #####
# X,Y,G,H,F A RENOMMER

class Cellule():

    def __init__(self, *args):
        self.atteignable = args[2]
        self.x = args[0]
        self.y = args[1]
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def getHeuristic(self, arriver):
        return 10 * (abs(self.x - arriver.x) + abs(self.y - arriver.y))