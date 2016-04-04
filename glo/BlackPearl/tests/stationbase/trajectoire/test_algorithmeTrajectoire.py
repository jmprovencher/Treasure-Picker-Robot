from unittest import TestCase
from stationbase.trajectoire.AlgorithmeTrajectoire import AlgorithmeTrajectoire
from elements.Carte import Carte
import random


class TestAlgorithmeTrajectoire(TestCase):
    def setUp(self):
        self.carte = Carte()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.trajectoire.initGrilleCellule([])
        self.algo = AlgorithmeTrajectoire(self.carte.trajectoire.grilleCellule)

    def test_trouverTrajet(self):
        depart = (random.randrange(5,1595), random.randrange(5,845))
        arrive = (random.randrange(5,1595), random.randrange(5,845))
        self.algo.trouverTrajet(depart, arrive)
        bool = self.trajetValide(self.carte.trajectoire.tra, depart, arrive)

        self.assertTrue(bool)

    def trajetValide(self, trajet, arrive, depart):
        if (trajet == []):
            return True
        elif (depart[0]-6 < trajet[0][0] and trajet[0][0] < depart[0]+6) and (depart[1]-9 < trajet[1][1] and trajet[1][1] < depart[1]+9):
            return True
        else:
            return False

    def test_simplifierTrajectoire(self):
        depart = (20, 20)
        milieuInutile = (20, 400)
        arrive = (20, 820)
        self.algo.trajet = [depart, milieuInutile, arrive]
        self.algo.simplifierTrajet()

        self.assertEqual(len(self.carte.trajectoire.trajectoire), 2)

    def test_SectionnerTrajectoire(self):
        depart = (20, 20)
        arrive = (20, 820)
        self.algo.trajet = [depart, arrive]
        self.algo.sectionnerTrajet()
        bool = len(self.algo.trajet) >= 2

        self.assertTrue(bool)

    def test_eliminerDetourInutile(self):
        depart = (20, 20)
        milieuInutile = (200, 400)
        arrive = (20, 820)
        self.algo.trajet = [depart, milieuInutile, arrive]
        self.algo.eliminerDetourInutile()
        bool = len(self.algo.trajet) == 2

        self.assertTrue(bool)

    def test_distanceAuCarre(self):
        self.algo.distanceAuCarre(0, 0, 8, 8)
        self.assertTrue(self.algo.grilleCellule.distanceAuCarre.called)

