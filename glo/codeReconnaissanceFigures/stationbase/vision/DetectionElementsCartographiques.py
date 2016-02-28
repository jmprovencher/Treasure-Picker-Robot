# import the necessary packages
import cv2
import numpy as np
import ConfigPath


class DetectionElementsCartographiques(object):
    def __init__(self, image):
        self.imageCamera = image
        self.patronTriangle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/triangle.png'), 0)
        self.patronCercle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        self.patronCarre = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        self.patronPentagone = cv2.imread(ConfigPath.Config().appendToProjectPath('images/pentagone.png'), 0)

        self.formesConnues = []
        self.ilesIdentifiees = []
        self.tresorIdentifies = []
        self.nombreFormes = 0
        self.nombreIles = 0

        self.intervalleRouge = np.array([100, 65, 200]), np.array([15, 0, 75]), "Rouge"
        self.intervalleBleu = np.array([255, 255, 102]), np.array([102, 102, 0]), "Bleu"
        self.intervalleJaune = np.array([51, 216, 242]), np.array([10, 120, 140]), "Jaune"
        self.intervalleVert = np.array([102, 255, 102]), np.array([0, 102, 0]), "Vert"

        self._definirPatronsFormes()

    def _definirPatronsFormes(self):
        precision, threshTriangle = cv2.threshold(self.patronTriangle, 127, 255, 0)
        precision, threshCercle = cv2.threshold(self.patronCercle, 127, 255, 0)
        precision, threshCarre = cv2.threshold(self.patronCarre, 127, 255, 0)
        precision, threshPentagone = cv2.threshold(self.patronPentagone, 127, 255, 0)

        _, contoursTriangle, _ = cv2.findContours(threshTriangle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntTriangle = contoursTriangle[0]
        _, contoursCercle, _ = cv2.findContours(threshCercle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCercle = contoursCercle[0]
        _, contoursCarre, _ = cv2.findContours(threshCarre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCarre = contoursCarre[0]
        _, contoursPentagone, _ = cv2.findContours(threshPentagone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntPentagone = contoursPentagone[0]

        self.formesConnues.append(self.cntTriangle)
        self.formesConnues.append(self.cntCarre)
        self.formesConnues.append(self.cntCercle)
        self.formesConnues.append(self.cntPentagone)

    def _trouverForme(self, contours, couleur):

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntTriangle, 1, 0.0), contours, "Triangle"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCercle, 1, 0.0), contours, "Cercle"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCarre, 1, 0.0), contours, "Carre"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntPentagone, 1, 0.0), contours, "Pentagone"))

        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme, couleur

        if (precision < 0.2):
            self.ilesIdentifiees.append(formeIdentifiee)
            self.nombreFormes += 1
        else:
            print "Forme non conforme detectee"

    def detecterIles(self):
        self._detecterFormeCouleur(self.intervalleRouge)
        self._detecterFormeCouleur(self.intervalleBleu)
        self._detecterFormeCouleur(self.intervalleJaune)
        self._detecterFormeCouleur(self.intervalleVert)

    def _detecterFormeCouleur(self, intervalleCouleur):

        intervalleClair, intervalleFonce, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contoursNegligeable = []
        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            if ((aire < 1000) or (aire > 6000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        for contoursForme in contoursCouleur:
            self._trouverForme(contoursForme, couleurForme)

    def detecterTresor(self):

        intervalleClair = np.array([37, 145, 145])
        intervalleFoncer = np.array([6, 100, 100])
        shapeTresorMasque = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)
        _, contoursTresor, _ = cv2.findContours(shapeTresorMasque.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contoursNegligeable = []
        for contours in range(len(contoursTresor)):
            aire = cv2.contourArea(contoursTresor[contours])
            if (aire < 30 or aire > 150):
                contoursNegligeable.append(contours)

        if (contoursNegligeable != []):
            contoursTresor = np.delete(contoursTresor, contoursNegligeable)

        for contours in contoursTresor:
            formeTresor = contours, "Tresor", ""
            print "Ajout tresor"
            self.tresorIdentifies.append(formeTresor)

    def _getNombreIleCouleur(self, couleurVoulue):
        nombreIles = 0
        for iles in self.ilesIdentifiees:
            _, _, couleur = iles
            if (couleur == couleurVoulue):
                nombreIles += 1
        return nombreIles
