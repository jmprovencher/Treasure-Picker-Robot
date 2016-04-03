from unittest import TestCase
import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from mock.mock import Mock, MagicMock


class TestDetectionIle(TestCase):

    def setUp(self):
        self.carreBleu = cv2.imread(ConfigPath.Config().appendToProjectPath('ilebleue.png'))
        self.pentagoneBleu = cv2.imread(ConfigPath.Config().appendToProjectPath('pentagonebleu.png'))

    def test_detection_ile_effectue_filtrage_couleur(self):
        detectionIle = DetectionIle(None)
        detectionIle.detecterFormeCouleur = MagicMock()
        detectionIle.detecterIle('vert')
        self.assertTrue(detectionIle.detecterFormeCouleur.called)

    def test_detection_ile_devant_retourne_un_ajustement(self):
        detectionIle = DetectionIle(self.carreBleu)
        detectionIle.detecterIle('bleu')
        ajustements = detectionIle.ajustements
        self.assertEqual(len(ajustements), 1, "Mauvais nombre d'ajustements avec ile bien alignee")

    def test_detection_ile_mal_alignee_retourne_deux_ajustements(self):
        detectionIle = DetectionIle(self.pentagoneBleu)
        detectionIle.detecterIle('bleu')
        ajustements = detectionIle.ajustements
        self.assertEqual(len(ajustements), 2, "Mauvais nombre d'ajustements avec ile mal alignee")
