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
        self.main()

    def initCarte(self):
        elementCartographiques = self.m_analyseImageWorld.getElementCartographiques()
        m_carte = Carte(elementCartographiques)

    def main(self):
        self.m_analyseImageWorld.trouverElement()
        self.initCarte()
