from unittest import TestCase
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.vision.DetectionRobot import DetectionRobot


class DetectionRbot(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.analyseImageWorld.chargerImage('images/table2/robotTest1.png')
        self.detection = DetectionRobot(self.analyseImageWorld.image, 2)

    def test_detecter(self):
        self.detection.detecter()

        self.assertIsNotNone(self.detection.robotIdentifiee)

    def test_trouverContoursRobot(self):
        c, h = self.detection.trouverContoursRobot()
        bool = len(c) >= 2

        self.assertTrue(bool)

    def test_trouverRobot(self):
        c, h = self.detection.trouverContoursRobot()
        c = self.detection.eleminerCoutoursNegligeable(c, h)
        self.detection.trouverRobot(c)

        self.assertIsNotNone(self.detection.robotIdentifiee)

    def test_eleminerCoutoursNegligeable(self):
        c, h = self.detection.trouverContoursRobot()
        c2 = self.detection.eleminerCoutoursNegligeable(c, h)
        bool = len(c2) <= len(c)

        self.assertTrue(bool)
          

