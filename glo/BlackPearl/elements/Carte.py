# import the necessary packages
from Tresor import Tresor

from elements.Ile import Ile
from stationbase.trajectoire.Trajectoire import Trajectoire
from elements.StationRecharge import StationRecharge
from elements.Cible import Cible

class Carte():
    def __init__(self):
        self.listeIles = []
        self.listeTresors = []
        self.infoRobot = None
        self.cible = Cible([self])
        self.stationRecharge = StationRecharge()
        self.trajectoire = Trajectoire()

    def ajouterElementCarto(self, elementCartographiques):
        for elementCarte in elementCartographiques:
            if (isinstance(elementCarte, Ile)):
                self.listeIles.append(elementCarte)

            elif (isinstance(elementCarte, Tresor)):
                self.listeTresors.append(elementCarte)

    def getIles(self):
        return self.listeIles

    def getIlesIndice(self, informationIleCible):
        retour = []
        for ile in self.listeIles:
            if (ile.couleur == informationIleCible or ile.forme == informationIleCible):
                retour.append(ile)
                print "ILE CIBLE"
                print ile.forme
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
