from stationbase.trajectoire.AlgorithmeTrajectoire import AlgorithmeTrajectoire
from stationbase.trajectoire.GrilleCellule import GrilleCellule


class Trajectoire:
    def __init__(self):
        self.grilleCellule = GrilleCellule()
        self.trajectoire = []

    def initGrilleCellule(self, listeIles):
        self.grilleCellule.initGrilleCellule(listeIles)

    def trouverTrajet(self, depart, arriver, type):
        algoTrajectoire = AlgorithmeTrajectoire(self.grilleCellule)
        self.trajectoire = algoTrajectoire.trouverTrajet(depart, arriver, type)
        return self.trajectoire

    def trouverLongueurTrajetCarre(self, trajet):
        distance = 0
        for i in range(1, len(trajet)):
            distance += self.distanceAuCarre(trajet[i - 1][0], trajet[i - 1][1], trajet[i][0], trajet[i][1])
        return distance

    def distanceAuCarre(self, x, y, destX, destY):
        return self.grilleCellule.distanceAuCarre(x, y, destX, destY)

    def depPixelXACentimetre(self, distanceX):
        return self.grilleCellule.depPixelXACentimetre(distanceX)

    def depPixelYACentimetre(self, distanceY):
        return self.grilleCellule.depPixelXACentimetre(distanceY)
