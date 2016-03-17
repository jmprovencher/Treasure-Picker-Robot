from unittest import TestCase
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from elements.Carte import Carte
import random


class TestAlgorithmeTrajectoire(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.analyseImageWorld.chargerImage('images/table2/trajet2.png')
        self.analyseImageWorld.trouverElementsCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)

    def test_trouverTrajet(self):
        depart = (random.randrange(5,1595), random.randrange(5,845))
        arrive = (random.randrange(5,1595), random.randrange(5,845))
        self.carte.trajectoire.trouverTrajet(depart, arrive)
        bool = self.trajetValide(self.carte.trajectoire.trajectoire, depart, arrive)

        self.assertEqual(bool, True)

    def trajetValide(self, trajet, arrive, depart):
        if (trajet == []):
            return True
        elif (depart[0]-6 < trajet[0][0] and trajet[0][0] < depart[0]+6) and (depart[1]-9 < trajet[1][1] and trajet[1][1] < depart[1]+9):
            return True
        else:
            return False

    def test_simplifierTrajectoire(self):
        depart = (20, 20)
        arrive = (20, 820)
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.carte.trajectoire.trouverTrajet(depart, arrive)

        self.assertEqual(len(self.carte.trajectoire.trajectoire), 2)


