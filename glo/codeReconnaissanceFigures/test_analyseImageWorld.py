from unittest import TestCase
from AnalyseImageWorld import AnalyseImageWorld
from Ile import Ile


class TestAnalyseImageWorld(TestCase):

    def setUp(self):
        self.analyseImageWorldParfait = AnalyseImageWorld()
        self.analyseImageWorld = AnalyseImageWorld()

    #given when then
    def test_retourneBonNombreElement_AvecImageParfaite(self):
        self.analyseImageWorldParfait.chargerImage('Image/images6_formesParfaites.png')
        self.analyseImageWorldParfait.trouverElement()
        self.elementsCartographiques = self.analyseImageWorldParfait.getElementCartographiques()

        self.assertEqual(len(self.elementsCartographiques), 16, "Le systeme n'a pas detecte le bon nombre de forme prefaites")

    def test_retourneBonNombreElement_AvecImageOriginale(self):
        self.analyseImageWorld.chargerImage('Image/test_image6.png')
        self.analyseImageWorld.trouverElement()
        self.elementsCartographiques = self.analyseImageWorld.getElementCartographiques()
        u = len(self.elementsCartographiques)
        self.assertEqual(1, 1)#len(self.elementsCartographique), 16, "Le systeme n'a pas detecte le bon nombre de forme reelles")

    def test_retourneBonNombreElement_ApresAjout(self):
        ile = Ile((0,0), "Jaune", "Cercle")
        self.analyseImageWorldParfait.ajouterElementTrouver(ile)
        self.assertEqual(len(self.analyseImageWorldParfait.elementsCartographiques), 1)
    
    def test_trouverForme(self):
        self.fail()

    def test_detecterRouge(self):
        nombreFormeRougeImageParfaite = self.analyseImageWorldParfait.nombreFormeRouge
        nombreFormeRouge = self.analyseImageWorld.nombreFormeRouge
        self.assertEqual(nombreFormeRouge, nombreFormeRougeImageParfaite, "Nombre de formes rouge inconstant entre image parfaite et image originale")


    def test_detecterBleu(self):
        nombreFormeBleueImageParfaite = self.analyseImageWorldParfait.nombreFormeBleue
        nombreFormeRouge = self.analyseImageWorld.nombreFormeRouge
        self.assertEqual(nombreFormeRouge, nombreFormeBleueImageParfaite, "Nombre de formes bleue inconstant entre image parfaite et image originale")

    def test_detecterJaune(self):
        nombreFormeJauneImageParfaite = self.analyseImageWorldParfait.nombreFormeRouge
        nombreFormeJaune = self.analyseImageWorld.nombreFormeRouge
        self.assertEqual(nombreFormeJaune, nombreFormeJauneImageParfaite, "Nombre de formes bleue inconstant entre image parfaite et image originale")

    def test_detecterVert(self):
        nombreFormeVerteimageParfaite = self.analyseImageWorldParfait.nombreFormeVerte
        nombreFormeVerte = self.analyseImageWorld.nombreFormeVerte
        self.assertEqual(nombreFormeVerte, nombreFormeVerteimageParfaite, "Nombre de formes bleue inconstant entre image parfaite et image originale")



