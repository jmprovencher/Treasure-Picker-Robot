# import the necessary packages
from stationbase.trajectoire.AlgorithmeTrajectoire import AlgorithmeTrajectoire
from stationbase.trajectoire.GrilleCellule import GrilleCellule


class Trajectoire():
    def __init__(self):
        self.grilleCellule = GrilleCellule()
        self.trajectoire = []

    def initGrilleCellule(self, listeIles):
        self.grilleCellule.initGrilleCellule(listeIles)

    def trouverTrajet(self, depart, arriver):
        algoTrajectoire = AlgorithmeTrajectoire(self.grilleCellule)
        self.trajectoire = algoTrajectoire.trouverTrajet(depart, arriver)
        return self.trajectoire

    def trouverLongueurTrajetPixCarre(self, trajet):
        distance = 0
        for i in range(1, len(trajet)):
            distance = distance + self.distanceADestinationAuCarre(trajet[i-1][0], trajet[i-1][1], trajet[i][0], trajet[i][1])
        return distance

    def distanceADestinationAuCarre(self, x, y, destX, destY):
        distanceX = destX - x
        distanceY = destY - y
        distanceX = self.grilleCellule.depPixelXACentimetre(distanceX)
        distanceY = self.grilleCellule.depPixelYACentimetre(distanceY)
        distanceCarre = distanceX**2 + distanceY**2
        return distanceCarre

    def afficherTrajectoire(self):
        print "\n******************************************************************************"
        print "Trajectoire:"
        print "******************************************************************************\n"
        if (self.trajectoire == []):
            print "Il n'existe aucun trajet!"
        else:
            print "Arriver!!"
            for deplacement in self.trajectoire:
                print "cellule: %d, %d" % deplacement
            print "Debut!!"
