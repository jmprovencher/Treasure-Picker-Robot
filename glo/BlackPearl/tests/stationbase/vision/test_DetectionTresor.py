from unittest import TestCase
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.vision.DetectionTresors import DetectionTresors
from elements.Tresor import Tresor


class DetectionTresor(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')
        self.detection = DetectionTresors(self.analyseImageWorld.image, 2)

    def test_detecter(self):
        self.detection.detecter()
        nombreTresor = len(self.detection.tresorIdentifies)

        self.assertEqual(nombreTresor, 3)

    def test_trouverContourTresors(self):
        c = self.detection.trouverContoursTresors()
        bool = len(c) >= 3

        self.assertTrue(bool)

    def test_trouverTresors(self):
        c = self.detection.trouverContoursTresors()
        self.detection.trouverTresors(c)
        bool = len(self.detection.tresorIdentifies) == len(c)

        self.assertTrue(bool)

    def test_eliminerTresorsImpossible(self):
        self.detection.tresorIdentifies.append(Tresor(500, 500))
        self.detection.eliminerTresorsImpossibles()
        bool = self.detection.tresorIdentifies == []

        self.assertTrue(bool)

    def test_eleminerCoutoursNegligeable(self):
        c, h = self.detection.trouverContoursTresors()
        c2 = self.detection.eleminerCoutoursNegligeables(c)
        bool = len(c2) <= len(c)

        self.assertTrue(bool)
