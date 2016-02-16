# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor

class Carte():

    def __init__(self):
        self.listeIles = []
        self.listeTresors = []

    def ajouterElementCarto(self,elementCartographiques):
        for elementCarte in elementCartographiques:
            if (isinstance(elementCarte, Ile)):
                self.listeIles.append(elementCarte)
            elif (isinstance(elementCarte, Tresor)):
                self.listeTresors.append(elementCarte)

    def getIles(self):
        return self.listeIles

    def getIles(self, couleurOuForme):
        retour = []
        for ile in self.listeIles:
            if (ile.getCouleur() == couleurOuForme):
                retour += ile
        return retour

    def getTresor(self):
        return self.m_tresor

    def afficherCarte(self):
        for ile in self.listeIles:
            ile.afficher()
        for tresor in self.listeTresors:
            tresor.afficher()
