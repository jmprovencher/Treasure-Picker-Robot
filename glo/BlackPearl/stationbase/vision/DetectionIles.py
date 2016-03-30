# import the necessary packages
import cv2
import numpy as np
import ConfigPath


class DetectionIles(object):
    def __init__(self, image):
        self.imageCamera = image
        self.formesConnues = []
        self.ilesIdentifiees = []
        self.nombreIles = 0
        self._definirIntervallesCouleurs()
        self._definirPatronsFormes()

    def detecter(self):
        self._detecterFormeCouleur(self.intervalleRouge)
        self._detecterFormeCouleur(self.intervalleBleu)
        self._detecterFormeCouleur(self.intervalleJaune)
        self._detecterFormeCouleur(self.intervalleVert)

    def _trouverForme(self, contours, couleur):

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntTriangle, 1, 0.0), contours, "Triangle"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCercle, 1, 0.0), contours, "Cercle"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCarre, 1, 0.0), contours, "Carre"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntPentagone, 1, 0.0), contours, "Pentagone"))

        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme, couleur

        if (precision < 0.1):
            print (nomForme, couleur, precision)
            self.ilesIdentifiees.append(formeIdentifiee)
            self.nombreIles += 1
        #else:
        #    print "Forme non conforme detectee"

    def _detecterFormeCouleur(self, intervalleCouleur):

        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        #cv2.imshow(couleurForme, masqueCouleur)
        _, contoursCouleur, hierarchy = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for i in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[i])
            if ((aire < 2000) or (aire > 6000)) and hierarchy[0][i][2]<0:
                contoursNegligeable.append(i)
            else:
                aireTrou = 0
                enfant = hierarchy[0][i][2]
                if cv2.contourArea(contoursCouleur[hierarchy[0][i][2]]) > 50:
                    contoursNegligeable.append(i)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)
        #a checker avec table si ca plante
        if len(contoursCouleur) < 10:
            for contoursForme in contoursCouleur:
                self._trouverForme(contoursForme, couleurForme)

    def _getNombreIleCouleur(self, couleurVoulue):
        nombreIles = 0
        for iles in self.ilesIdentifiees:
            _, _, couleur = iles
            if (couleur == couleurVoulue):
                nombreIles += 1
        return nombreIles

    def _definirIntervallesCouleurs(self):
        self.intervalleRouge = np.array([15, 0, 75]), np.array([100, 65, 200]),"Rouge"
        self.intervalleBleu = np.array([102, 102, 0]), np.array([255, 255, 102]), "Bleu"
        self.intervalleJaune = np.array([0, 50, 50]), np.array([50, 255, 255]), "Jaune"
        self.intervalleVert = np.array([0, 102, 0]), np.array([102, 255, 102]), "Vert"

    def _definirPatronsFormes(self):
        patronTriangle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/triangle.png'), 0)
        patronCercle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        #cv2.imshow('test2', patronCercle)
        #cv2.waitKey(0)
        patronCarre = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        patronPentagone = cv2.imread(ConfigPath.Config().appendToProjectPath('images/pentagone.png'), 0)

        precision, threshTriangle = cv2.threshold(patronTriangle, 127, 255, 0)
        precision, threshCercle = cv2.threshold(patronCercle, 127, 255, 0)
        precision, threshCarre = cv2.threshold(patronCarre, 127, 255, 0)
        precision, threshPentagone = cv2.threshold(patronPentagone, 127, 255, 0)

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

