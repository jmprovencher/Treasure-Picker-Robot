from unittest import TestCase
from robot.interface.Robot import Robot
from mock import Mock, MagicMock, mock
from robot.communication.LectureUART import LectureUART
from robot.communication.UARTDriver import UARTDriver

class TestLectureUART(TestCase):

    def setUp(self):
        uartDriver = Mock(spec=UARTDriver)
        self.robot = Robot(uartDriver)

        self.lectureUART = LectureUART(self.robot)

    def test_lecture_code_manchester_retourne_lettre_decoder(self):
        self.lectureUART.analyserLecture('aaaa')
        self.assertTrue(self.robot.lettreObtenue)

    def test_lecture_lettre_melangee_retourne_aucune_lettre(self):
        self.lectureUART.analyserLecture('abcd')
        self.assertFalse(self.robot.lettreObtenue)

    def test_lecture_done_envoie_commande_terminee(self):
        self.lectureUART.analyserLecture('done')
        self.assertTrue(self.robot.commandeTerminee)

    def test_lecture_tension_condensateur_maj_tension(self):
        self.lectureUART.analyserLecture(1.7)
        self.assertEquals(self.robot.tensionCondensateur, 1.7)