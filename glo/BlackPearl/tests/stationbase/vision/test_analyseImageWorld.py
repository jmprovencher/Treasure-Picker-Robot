from unittest import TestCase

from elements.Ile import Ile
from elements.Tresor import Tresor
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld


class TestAnalyseImageWorld(TestCase):
    def setUp(self):
        self.analyseImageWorld = AnalyseImageWorld()

    def test_retourne_bon_nombre_elements_apres_ajout(self):
        ile = Ile((0, 0), "Jaune", "Cercle")
        tresor = Tresor((0, 0))
        self.analyseImageWorld.elementsCartographiques.append(ile)
        self.analyseImageWorld.elementsCartographiques.append(tresor)

        self.assertEqual(len(self.analyseImageWorld.elementsCartographiques), 2)

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

    def test_chargement_image(self):
        self.analyseImageWorld.chargerImage('images/table2/detection1.png')
        self.assertIsNotNone(self.analyseImageWorld.imageCamera)
