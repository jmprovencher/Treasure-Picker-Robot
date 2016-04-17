from unittest import TestCase
from robot.alignement.AlignementStation import AlignementStation
from mock import Mock, MagicMock

class TestAlignementStation(TestCase):
    def setUp(self):
        self.alignementStation = AlignementStation()

    def test_distance_laterale_negative_retourne_deplacement_gauche(self):
        distance_x = -2
        commande, _ = self.alignementStation.ajusterPositionLaterale_CM(distance_x)
        self.assertEqual('left', commande, "Station se trouvant a gauche, mais retourne un deplacement a droite")

    def test_distance_laterale_positive_retourne_deplacement_droite(self):
        distance_x = 3
        commande, _ = self.alignementStation.ajusterPositionLaterale_CM(distance_x)
        self.assertEqual('right', commande, "Station se trouvant a droite, mais retourne un deplacement a gauche")

    def test_distance_frontale_positive_retourne_deplacement_avant(self):
        distance_y = 3
        commande, _ = self.alignementStation.ajusterPositionY(distance_y)
        self.assertEqual('forward', commande, "Station se trouvant en avant, mais retourne un deplacement recule")

    def test_distance_elevee_retourne_deux_ajustements(self):
        distance_x = 4
        distance_y = 3
        ajustements = self.alignementStation.calculerAjustement(distance_x, distance_y)
        self.assertEqual(len(ajustements), 2, "Station mal alignee, mais ne retourne pas le bon nombre d'ajustement")

    def test_distance_laterale_en_mm_negligeable_retourne_aucun_ajustements_en_mm(self):
        distance_x = 1.2
        distance_y = 3
        self.alignementStation.ajusterPositionLaterale_MM = MagicMock()
        ajustements = self.alignementStation.calculerAjustement(distance_x, distance_y)
        self.assertFalse(self.alignementStation.ajusterPositionLaterale_MM.called)

    def test_distance_laterale_minimale_retourne_ajustements_en_mm(self):
        distance_x = 1.4
        distance_y = 5
        self.alignementStation.ajusterPositionLaterale_MM = MagicMock()
        ajustements = self.alignementStation.calculerAjustement(distance_x, distance_y)
        self.assertTrue(self.alignementStation.ajusterPositionLaterale_MM.called)

    def test_distance_laterale_grande_retourne_ajustements_en_cm_seulement(self):
        distance_x = 32.8
        distance_y = 5
        self.alignementStation.ajusterPositionLaterale_MM = MagicMock()
        ajustements = self.alignementStation.calculerAjustement(distance_x, distance_y)
        self.assertFalse(self.alignementStation.ajusterPositionLaterale_MM.called)