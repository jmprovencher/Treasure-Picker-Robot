from unittest import TestCase
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.Robot import Robot
from mock.mock import Mock, MagicMock

class TestAnalyseImageEmbarquee(TestCase):

    def setUp(self):
        self.robot = Mock(spec=Robot)

    def test_parametre_tresor_demarre_analyse_tresor(self):
        self.analyseImage = AnalyseImageEmbarquee(self.robot)
        self.analyseImage.evaluerPositionTresor = MagicMock()
        self.analyseImage.debuterAlignement('tresor')
        self.assertTrue(self.analyseImage.evaluerPositionTresor.called)

    def test_parametre_couleur_demarre_analyse_depot(self):
        self.analyseImage = AnalyseImageEmbarquee(self.robot)
        self.analyseImage.evaluerPositionDepot = MagicMock()
        self.analyseImage.debuterAlignement(3)
        self.assertTrue(self.analyseImage.evaluerPositionDepot.called)

    def test_parametre_station_demarre_analyse_station(self):
        self.analyseImage = AnalyseImageEmbarquee(self.robot)
        self.analyseImage.evaluerPositionStation = MagicMock()
        self.analyseImage.debuterAlignement('station')
        self.assertTrue(self.analyseImage.evaluerPositionStation.called)

