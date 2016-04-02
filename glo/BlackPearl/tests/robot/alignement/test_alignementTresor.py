from unittest import TestCase
from robot.alignement.AlignementTresor import AlignementTresor

class TestAlignementTresor(TestCase):

    def setUp(self):
        self.positionZoneDepot = (800, 850)
        self.alignementTresor = AlignementTresor()

    def test_distance_laterale_negative_retourne_deplacement_gauche(self):
        distance_x = -200
        commande, _ = self.alignementTresor.ajusterPositionX(distance_x)
        self.assertEqual('left', commande, "Tresor se trouvant a gauche, mais retourne un deplacement a droite")

    def test_distance_laterale_positive_retourne_deplacement_droite(self):
        distance_x = 300
        commande, _ = self.alignementTresor.ajusterPositionX(distance_x)
        self.assertEqual('right', commande, "Tresor se trouvant a droite, mais retourne un deplacement a gauche")

    def test_distance_frontale_positive_retourne_deplacement_avant(self):
        distance_y = 300
        commande, _ = self.alignementTresor.ajusterPositionY(distance_y)
        self.assertEqual('forward', commande, "tresor se trouvant en avant, mais retourne un deplacement recule")

    def test_distance_elevee_retourne_deux_ajustements(self):
        distance_x = 400
        distance_y = 320
        ajustements = self.alignementTresor.calculerAjustement(distance_x, distance_y)
        self.assertEqual(len(ajustements), 2,
                         "Tresor mal aligne, mais ne retourne pas le bon nombre d'ajustement")

    def test_distance_laterale_negligeable_retourne_ajustement_frontal_seulement(self):
        distance_x = 5
        distance_y = 320
        ajustements = self.alignementTresor.calculerAjustement(distance_x, distance_y)
        self.assertEquals(len(ajustements), 1,
                          "Tresor est alignee devant le robot, mais un alignement lateral est calculer")
