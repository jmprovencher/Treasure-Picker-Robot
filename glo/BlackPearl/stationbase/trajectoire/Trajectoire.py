from stationbase.trajectoire.AlgorithmeTrajectoire import AlgorithmeTrajectoire
from stationbase.trajectoire.GrilleCellule import GrilleCellule


class Trajectoire:
    def __init__(self):
        self.grilleCellule = GrilleCellule()
        self.trajectoire = []

    def initGrilleCellule(self, listeIles):
        self.grilleCellule.initGrilleCellule(listeIles)

    def trouverTrajet(self, depart, arriver):
        algoTrajectoire = AlgorithmeTrajectoire(self.grilleCellule)
        self.trajectoire = algoTrajectoire.trouverTrajet(depart, arriver)
        return self.trajectoire

    def trouverLongueurTrajetCarre(self, trajet):
        distance = 0
        for i in range(1, len(trajet)):
            distance = distance + self.distanceAuCarre(trajet[i - 1][0], trajet[i - 1][1], trajet[i][0], trajet[i][1])
        return distance

    def distanceAuCarre(self, x, y, destX, destY):
        return self.grilleCellule.distanceAuCarre(x, y, destX, destY)

    def depPixelXACentimetre(self, distanceX):
        self.grilleCellule.depPixelXACentimetre(distanceX)

    def depPixelYACentimetre(self, distanceY):
        self.grilleCellule.depPixelXACentimetre(distanceY)
