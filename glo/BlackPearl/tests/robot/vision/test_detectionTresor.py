from unittest import TestCase
import cv2
import ConfigPath
from robot.vision.DetectionTresor import DetectionTresor
from mock.mock import Mock, MagicMock

class TestDetectionTresor(TestCase):
    def setUp(self):
        self.tresor = cv2.imread(ConfigPath.Config().appendToProjectPath('testtresor.png'))

    def test_detection_tresor_gauche_retourne_deux_ajustements(self):
        detectionTresor = DetectionTresor(self.tresor)
        detectionTresor.calculerAjustements()
        ajustements = detectionTresor.ajustements
        self.assertEqual(len(ajustements), 2)

    def test_detection_tresor_gauche_retourne_ajustements_gauche(self):
        detectionTresor = DetectionTresor(self.tresor)
        detectionTresor.calculerAjustements()
        ajustements = detectionTresor.ajustements
        self.assertTrue([ajusts for ajusts in ajustements if 'left' in ajusts])
        self.assertTrue([ajusts for ajusts in ajustements if 'forward' in ajusts])