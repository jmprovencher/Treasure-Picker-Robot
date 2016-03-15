from unittest import TestCase
import cv2
import ConfigPath

from stationbase.vision.DetectionIles import DetectionIles


class TestDetectionElementsCartographiques(TestCase):
    def setUp(self):
        self.image = self.imageCamera = cv2.imread(
            ConfigPath.Config().appendToProjectPath('images/table2/detection1.png'))
        self.detectionElements = DetectionIles(self.image)

    def test_detecte_bon_nombre_de_formes_jaune(self):
        self.detectionElements.detecter()
        nombreJaune = self.detectionElements._getNombreIleCouleur("Jaune")
        self.assertEqual(nombreJaune, 4)

    def test_detecte_bon_nombre_de_formes_bleue(self):
        self.detectionElements.detecter()
        nombreBleu = self.detectionElements._getNombreIleCouleur("Bleu")
        self.assertEqual(nombreBleu, 4)

    def test_detecte_bon_nombre_de_formes_verte(self):
        self.detectionElements.detecter()
        nombreVert = self.detectionElements._getNombreIleCouleur("Vert")
        self.assertEqual(nombreVert, 4)

    def test_detecte_bon_nombre_de_formes_rouge(self):
        self.detectionElements.detecter()
        nombreRouge = self.detectionElements._getNombreIleCouleur("Rouge")
        self.assertEqual(nombreRouge, 4)

    def test_detecte_bon_nombre_tresor(self):
        self.detectionElements.detecterTresor()
        tresors = self.detectionElements.tresorIdentifies
        self.assertEqual(len(tresors), 3)
