# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor
from Carte import Carte
from AnalyseImageWorld import AnalyseImageWorld

class StationBase():

    def __init__(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.main()

    def main(self):
        print "\n******************************************************************************"
        print "Details de detection"
        print "******************************************************************************\n"
        self.analyseImageWorld.trouverElement()
        elementCartographique = self.analyseImageWorld.getElementCartographiques()
        self.carte.ajouterElementCarto(elementCartographique)
        print "\n******************************************************************************"
        print "Carte virtuelle"
        print "******************************************************************************\n"
        self.carte.afficherCarte()

