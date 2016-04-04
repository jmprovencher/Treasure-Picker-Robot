from unittest import TestCase
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.vision.DetectionIles import DetectionIles


class DetectionIle(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')
        self.detection = DetectionIles(self.analyseImageWorld.image, 2)
        
    def test_detecter(self):
        self.detection.detecter()
        nombreTresor = len(self.detection.ilesIdentifiees)

        self.assertEqual(nombreTresor, 16)
        
    def test_trouverContourIles(self):
        c, h = self.detection.trouverContoursIles('Rouge')
        bool = len(c) >= 4
        
        self.assertTrue(bool)
        
    def test_trouverIles(self):
        c, h = self.detection.trouverContoursIles('Rouge')
        self.detection.trouverIles(c, h, 'Rouge')
        bool = len(self.detection.ilesIdentifiees) == len(c)
        
        self.assertTrue(bool)

    def test_eleminerCoutoursNegligeable(self):
        c, h = self.detection.trouverContoursIles('Rouge')
        c2 = self.detection.eleminerCoutoursNegligeable(c, h)
        bool = len(c2) <= len(c)

        self.assertTrue(bool)
        

