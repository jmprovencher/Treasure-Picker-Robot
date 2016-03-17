from unittest import TestCase
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from elements.Carte import Carte
from stationbase.trajectoire.AlgorithmeTrajectoire import AlgorithmeTrajectoire
from stationbase.trajectoire.GrilleCellule import GrilleCellule


class GrilleCellule(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.analyseImageWorld.chargerImage('images/table2/trajet2.png')
        self.analyseImageWorld.trouverElementsCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)

    def test_initGrilleCellule(self):
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)

        self.assertEqual(len(self.carte.trajectoire.grilleCellule.listeCellules), 34240)

    def test_xEstAtteignable(self):
        bool = self.carte.trajectoire.grilleCellule.xEstAtteignable(self.carte.listeIles[0].getX(), self.carte.listeIles)

        self.assertEqual(bool, False)

    def test_yEstAtteignable(self):
        bool = self.carte.trajectoire.grilleCellule.yEstAtteignable(self.carte.listeIles[0].getY(), self.carte.listeIles)

        self.assertEqual(bool, False)

    def test_getCellule(self):
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        cellule = self.carte.trajectoire.grilleCellule.getCellule(500,504)
        if cellule.x == 500 and cellule.y == 504:
            bool = True
        else:
            bool = False

        self.assertEqual(bool, True)


    def getCelluleAdjacentes(self, cellule):
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        cellule = self.carte.trajectoire.grilleCellule.getCellule(500,504)
        listeAdj = self.carte.trajectoire.grilleCellule.getCelluleAdjacentes(cellule)

        self.assertEqual(len(listeAdj), 8)

