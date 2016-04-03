from unittest import TestCase
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot
from mock import Mock, MagicMock

class TestRobot(TestCase):

    def setUp(self):
        uartDriver = Mock(spec=UARTDriver)
        self.robot = Robot(uartDriver)

    def test_demarrerAlignementIle(self):
        self.robot.demarrerAlignementIle = MagicMock()
        self.robot.traiterCommande('alignement_ile', 0)
        self.assertTrue(self.robot.demarrerAlignementIle.called)

    def test_demarrerAlignementStation(self):
        self.robot.demarrerAlignementStation = MagicMock()
        self.robot.traiterCommande('alignement_station', 0)
        self.assertTrue(self.robot.demarrerAlignementStation.called)

    def test_demarrerAlignementTresor(self):
        self.robot.demarrerAlignementTresor = MagicMock()
        self.robot.traiterCommande('alignement_tresor', 0)
        self.assertTrue(self.robot.demarrerAlignementTresor.called)
