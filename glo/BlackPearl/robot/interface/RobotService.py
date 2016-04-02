from robot.communication.islandServerRequest import islandServerRequest


class RobotService:
    def __init__(self):
        self.adresseIP = '192.168.0.2'
        self.indiceObtenu = None

    def obtenirCible(self, lettre):
        indice = self._effectuerRequeteServeur(lettre)
        cible = self._determinerCible(indice)
        return cible

    def _determinerCible(self, reponse):
        if "forme" in reponse:
            if "carre" in reponse:
                self.indiceObtenu = "carre"
            elif "pentagone" in reponse:
                self.indiceObtenu = "pentagone"
            elif "cercle" in reponse:
                self.indiceObtenu = "cercle"
            elif "triangle" in reponse:
                self.indiceObtenu = "triangle"
            else:
                print("Aucune cible determinee")
            self.pretEnvoyerIndice = True

        elif "couleur" in reponse:
            if "rouge" in reponse:
                self.indiceObtenu = "rouge"
            elif "bleu" in reponse:
                self.indiceObtenu = "bleu"
            elif "vert" in reponse:
                self.indiceObtenu = "vert"
            elif "jaune" in reponse:
                self.indiceObtenu = "jaune"
            else:
                print("Aucune cible determinee")
            self.pretEnvoyerIndice = True
        else:
            print("Erreur reponse du serveur")
        return self.indiceObtenu

    def _effectuerRequeteServeur(self, lettre):
        reponse = islandServerRequest(self.adresseIP, lettre)
        return reponse
