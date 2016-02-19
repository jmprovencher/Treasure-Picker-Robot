# import the necessary packages
import numpy as np
import heapq
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor
from Cellule import Cellule
from GrilleCellule import GrilleCellule
from AlgoAEtoile import AlgoAEtoile

class Trajectoire():

    def __init__(self):
        self.grilleCellule = GrilleCellule()
        self.trajet = []

    def initGrilleCellule(self, listeIles):
        self.grilleCellule.initGrilleCellule(listeIles)

    def trouverTrajet(self, depart, arriver):
        algo = AlgoAEtoile(self.grilleCellule)
        self.trajet = algo.trouverTrajet(depart, arriver)

    def afficherTrajectoire(self):
        print "\n******************************************************************************"
        print "Trajectoire:"
        print "******************************************************************************\n"
        if (self.trajet == []):
            print "Il n'existe aucun trajet!"
        else:
            print "Arriver!!"
            for deplacement in self.trajet:
                print "cellule: %d, %d" % deplacement
            print "Debut!!"



















