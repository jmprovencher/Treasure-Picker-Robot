# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor

class Carte():

    def __init__(self,elementCartographiques):
        m_iles = []
        m_tresors = []
        for elementCarto in elementCartographiques:
            if (elementCarto is Ile):
                m_iles += elementCarto
            elif (elementCarto is Tresor):
                m_tresors += elementCarto

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
