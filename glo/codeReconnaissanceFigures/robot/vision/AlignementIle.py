import cv2
import numpy as np
import ConfigPath


class AlignementIle(object):
    def __init__(self, image, couleurIleCible):
        self.imageCamera = image
        self.couleurIle = couleurIleCible
        self.detecterIle()
        self.formesConnues = []

        self._definirIntervallesCouleurs()
        self._definirPatronsFormes()
        #cv2.imshow("image", image)
        #self.definirPositionOptimale()

    def dessinerCercleDepot(self, positionCentre):
        cv2.circle(self.imageCamera, positionCentre,10,(0,255,0),2)
        cv2.imshow("Image", self.imageCamera)

    def detecterIle(self):
        if (self.couleurIle == "Vert"):
            self._detecterFormeCouleur(self.intervalleVert)
        elif (self.couleurIle == "Jaune"):
            self._detecterFormeCouleur(self.intervalleJaune)
        elif (self.couleurIle == "Bleu"):
            self._detecterFormeCouleur(self.intervalleBleu)
        elif (self.couleurIle == "Rouge"):
            self._detecterFormeCouleur(self.intervalleRouge)

    def _detecterFormeCouleur(self, intervalleCouleur):

        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        cv2.imshow(couleurForme, masqueCouleur)
        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            if ((aire < 1000) or (aire > 6000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        if len(contoursCouleur) < 10:
            for contoursForme in contoursCouleur:
                position = self.trouverCentreForme(contoursForme)
                self.dessinerCercleDepot(position)


    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])
        return centre_x, centre_y

    def _definirIntervallesCouleurs(self):
        self.intervalleRouge = np.array([15, 0, 75]), np.array([100, 65, 200]),"Rouge"
        self.intervalleBleu = np.array([102, 102, 0]), np.array([255, 255, 102]), "Bleu"
        self.intervalleJaune = np.array([0, 50, 50]), np.array([50, 255, 255]), "Jaune"
        self.intervalleVert = np.array([0, 102, 0]), np.array([102, 255, 102]), "Vert"

    def _definirPatronsFormes(self):
        patronTriangle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/triangle.png'), 0)
        patronCercle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
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