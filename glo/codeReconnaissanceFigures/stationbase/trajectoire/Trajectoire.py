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


