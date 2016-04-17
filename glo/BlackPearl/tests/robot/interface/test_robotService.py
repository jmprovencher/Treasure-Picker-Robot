from unittest import TestCase
from robot.interface.RobotService import RobotService

class TestRobotService(TestCase):

    def setUp(self):
        self.robotService = RobotService()

    def test_cible_determinee_avec_forme_en_indice(self):
        reponse = "{'forme': 'pentagone'}"
        self.robotService.determinerCible(reponse)
        self.assertEqual(self.robotService.indiceObtenu, 'pentagone')

    def test_cible_determinee_avec_couleur_en_indice(self):
        reponse = "{'couleur': 'rouge'}"
        self.robotService.determinerCible(reponse)
        self.assertEqual(self.robotService.indiceObtenu, 'rouge')

    def test_cible_non_determinee_avec_message_erronne(self):
        reponse = "{'couleur': 'showtime'}"
        self.robotService.determinerCible(reponse)
        self.assertIsNone(self.robotService.indiceObtenu)
