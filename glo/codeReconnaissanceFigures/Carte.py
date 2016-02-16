# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor

class Carte():

    def __init__(self):
        self.m_iles = []
        self.m_tresors = []

    def ajouterElementCarto(self,elementCartographiques):
        for elementCarto in elementCartographiques:
            if (isinstance(elementCarto, Ile)):
                self.m_iles.append(elementCarto)
            elif (isinstance(elementCarto, Tresor)):
                self.m_tresors.append(elementCarto)

    def getIles(self):
        return self.m_iles

    def getIles(self, couleurOuForme):
        retour = []
        for ile in self.m_iles:
            if (ile.getCouleur() == couleurOuForme):
                retour += ile
        return retour

    def getTresor(self):
        return self.m_tresor

    def afficherCarte(self):
        for ile in self.m_iles:
            ile.afficher()
        for tresor in self.m_tresors:
            tresor.afficher()
