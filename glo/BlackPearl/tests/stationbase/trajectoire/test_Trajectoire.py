from unittest import TestCase
from elements.Carte import Carte
import random


class Trajectoire(TestCase):
    def setUp(self):
        self.carte = Carte()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.trajectoire.initGrilleCellule([])

    def test_trouverTrajet(self):
        depart = (random.randrange(5,1595), random.randrange(5,845))
        arrive = (random.randrange(5,1595), random.randrange(5,845))
        self.carte.trajectoire.trouverTrajet(depart, arrive)
        bool = self.trajetValide(self.carte.trajectoire.tra, depart, arrive)

        self.assertTrue(bool)

    def trajetValide(self, trajet, arrive, depart):
        if (trajet == []):
            return True
        elif (depart[0]-6 < trajet[0][0] and trajet[0][0] < depart[0]+6) and (depart[1]-9 < trajet[1][1] and trajet[1][1] < depart[1]+9):
            return True
        else:
            return False

    def test_trouverLongueurTrajetCarre(self):
        depart = (0, 0)
        milieu = (0, 855)
        arrive = (0, 1600)
        trajet = [depart, milieu, arrive]
        dist = self.carte.trajectoire.trouverLongueurTrajetCarre(trajet)
        bool = 110**2 + 220**2 < dist < 120**2 + 230**2

        self.assertTrue(bool)

    def test_distanceAuCarre(self):
        self.algo.distanceAuCarre(0, 0, 8, 8)
        self.assertTrue(self.carte.trajectoire.grilleCellule.distanceAuCarre.called)

