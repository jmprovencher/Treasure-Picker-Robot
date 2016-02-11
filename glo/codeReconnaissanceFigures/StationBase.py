# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor
from Carte import Carte
from AnalyseImageWorld import AnalyseImageWorld

class StationBase():

    def __init__(self):
        self.m_analyseImageWorld = AnalyseImageWorld()
        self.m_carte = Carte()
        self.main()

    def main(self):
        print "\n******************************************************************************"
        print "Details de detection"
        print "******************************************************************************\n"
        self.m_analyseImageWorld.trouverElement()
        elementCarto = self.m_analyseImageWorld.getElementCartographiques()
        self.m_carte.ajouterElementCarto(elementCarto)
        print "\n******************************************************************************"
        print "Carte virtuelle"
        print "******************************************************************************\n"
        self.m_carte.afficherCarte()

