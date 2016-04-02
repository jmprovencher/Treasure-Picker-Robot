from unittest import TestCase
from robot.alignement.AlignementIle import AlignementIle


class TestAlignementIle(TestCase):
    def setUp(self):
        self.positionZoneDepot = (800, 850)
        self.alignementIle = AlignementIle()


    def test_distance_laterale_negative_retourne_deplacement_gauche(self):
        distance_x = -300
        commande, _ = self.alignementIle.ajusterPositionX(distance_x)
        self.assertEqual('left', commande, "Ile se trouvant a gauche, mais retourne un deplacement a droite")

    def test_distance_laterale_positive_retourne_deplacement_droite(self):
        distance_x = 500
        commande, _ = self.alignementIle.ajusterPositionX(distance_x)
        self.assertEqual('right', commande, "Ile se trouvant a droite, mais retourne un deplacement a gauche")

    def test_distance_frontale_positive_retourne_deplacement_avant(self):
        distance_y = 300
        commande, _ = self.alignementIle.ajusterPositionY(distance_y)
        self.assertEqual('forward', commande, "Ile se trouvant en avant, mais retourne un deplacement recule")

    def test_distance_elevee_retourne_deux_ajustements(self):
        distance_x = 400
        distance_y = 320
        ajustements = self.alignementIle.calculerAjustement(distance_x, distance_y)
        self.assertEqual(len(ajustements), 2, "Ile se trouvant hors de portee du robot, mais ne retourne pas le bon nombre d'ajustement")

    def test_distance_laterale_negligeable_retourne_ajustement_frontal_seulement(self):
        distance_x = 35
        distance_y = 320
        ajustements = self.alignementIle.calculerAjustement(distance_x, distance_y)
        self.assertEquals(len(ajustements), 1, "Ile est alignee devant le robot, mais un alignement lateral est calculer")

    def test_distance_negligeable_retourne_aucun_ajustement(self):
        distance_x = 35
        distance_y = 23
        ajustements = self.alignementIle.calculerAjustement(distance_x, distance_y)
        self.assertEquals(ajustements, [], "Ile deja alignee, mais un alignement a ete calcule")