# import the necessary packages
from Tresor import Tresor

from elements.Ile import Ile
from stationbase.trajectoire.Trajectoire import Trajectoire


class Carte():
    def __init__(self):
        self.listeIles = []
        self.listeTresors = []
        #self.trajectoire = Trajectoire()
        self.trajectoire = [(20, 130), (100, 100), (200, 400), (600, 200), (1000, 600)]

    def ajouterElementCarto(self, elementCartographiques):
        for elementCarte in elementCartographiques:
            if (isinstance(elementCarte, Ile)):
                self.listeIles.append(elementCarte)

            elif (isinstance(elementCarte, Tresor)):
                self.listeTresors.append(elementCarte)

    def getIles(self):
        return self.listeIles

    def getIles(self, informationIleCible):
        retour = []
        for ile in self.listeIles:
            if (ile.couleur == informationIleCible):
                retour += ile
        return retour

    def getTresor(self):
        return self.m_tresor

    def afficherCarte(self):
        print "\n******************************************************************************"
        print "Carte virtuelle"
        print "******************************************************************************\n"
        for ile in self.listeIles:
            ile.afficher()
        for tresor in self.listeTresors:
            tresor.afficher()
