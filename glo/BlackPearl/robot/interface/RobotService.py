from robot.communication.islandServerRequest import islandServerRequest

REPONSE_RECTANGLE = "rectangle"
REPONSE_PENTAGONE = "pentagone"
REPONSE_CERCLE = "cercle"
REPONSE_TRIANGLE = "triangle"
REPONSE_COULEUR = "couleur"
REPONSE_ROUGE = "rouge"
REPONSE_BLEU = "bleu"
REPONSE_VERT = "vert"
REPONSE_JAUNE = "jaune"


class RobotService:
    def __init__(self):
        self.adresseIPServeur = '192.168.0.2'
        self.indiceObtenu = None

    def obtenirCible(self, lettre):
        indice = self._effectuerRequeteServeur(lettre)
        print("INDICE OBTENU: %s" %indice)
        cible = self.determinerCible(indice)
        return cible

    def determinerCible(self, reponse):
        if "forme" in reponse:
            if REPONSE_RECTANGLE in reponse:
                self.indiceObtenu = "carre"
            elif REPONSE_PENTAGONE in reponse:
                self.indiceObtenu = REPONSE_PENTAGONE
            elif REPONSE_CERCLE in reponse:
                self.indiceObtenu = REPONSE_CERCLE
            elif REPONSE_TRIANGLE in reponse:
                self.indiceObtenu = REPONSE_TRIANGLE
            else:
                print("Aucune cible determinee")
            print reponse

        elif REPONSE_COULEUR in reponse:
            if REPONSE_ROUGE in reponse:
                self.indiceObtenu = REPONSE_ROUGE
            elif REPONSE_BLEU in reponse:
                self.indiceObtenu = REPONSE_BLEU
            elif REPONSE_VERT in reponse:
                self.indiceObtenu = REPONSE_VERT
            elif REPONSE_JAUNE in reponse:
                self.indiceObtenu = REPONSE_JAUNE
            else:
                print("Aucune cible determinee")
            print reponse
        else:
            print("Erreur reponse du serveur")
        return self.indiceObtenu

    def _effectuerRequeteServeur(self, lettre):
        reponse = islandServerRequest(self.adresseIPServeur, lettre)
        return reponse
