from unittest import TestCase
import cv2
import ConfigPath
from robot.vision.DetectionStation import DetectionStation
from mock import Mock, MagicMock, mock


class TestDetectionStation(TestCase):

    def setUp(self):
        self.stationRecharge= cv2.imread(ConfigPath.Config().appendToProjectPath('stationrecharge.png'))

    def test_detection_ile_devant_retourne_un_ajustement(self):
        detectionStation = DetectionStation()
        detectionStation.trouverAjustements(self.stationRecharge)
        ajustements = detectionStation.ajustements
        self.assertEqual(len(ajustements), 1)
