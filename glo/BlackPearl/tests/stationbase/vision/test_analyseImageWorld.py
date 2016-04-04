from unittest import TestCase
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld


class AnalyseImageWorld(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()

    def test_retourne_bon_nombre_total_elements_apres_detection(self):
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')
        self.analyseImageWorld.trouverElementsCartographiques()
        nombreElement = len(self.analyseImageWorld.elementsCartographiques)

        self.assertEqual(nombreElement, 19)

    def test_retourne_bon_nombre_tresors_apres_detection(self):
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')
        self.analyseImageWorld.trouverElementsCartographiques()
        nombreTresor = len(self.analyseImageWorld.tresorIdentifies)

        self.assertEqual(nombreTresor, 3)

    def test_retourne_bon_nombre_iles_apres_detection(self):
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')
        self.analyseImageWorld.trouverElementsCartographiques()
        nombreTresor = len(self.analyseImageWorld.ilesIdentifiees)

        self.assertEqual(nombreTresor, 16)

    def test_trouverRobot(self):
        self.analyseImageWorld.chargerImage('images/table2/robotTest1.png')
        self.analyseImageWorld.trouverRobot()

        self.assertIsNotNone(self.analyseImageWorld.robotIdentifie)

    def test_chargement_image(self):
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')

        self.assertIsNotNone(self.analyseImageWorld.imageCamera)

    def test_resultatPlusCommun(self):
        test = [[1, 2, 3, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3]]
        list = self.analyseImageWorld.resultatPlusCommun(test)
        bool = [1, 2, 3].__eq__(list)

        self.assertTrue(bool)
