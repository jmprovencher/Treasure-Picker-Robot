from __future__ import division
import cv2
import numpy as np
from robot.alignement.AlignementIle import AlignementIle


class DetectionIle(object):
    def __init__(self, image):
        self.alignementIle = AlignementIle()
        self.alignementTerminer = False
        self.imageCamera = image
        self.ajustements = []

        self.positionZone = (800, 850)
        self.rayonZone = 100

        self._definirIntervallesCouleurs()
        #self._dessinerZoneCible()

    def detecterIle(self, couleurIleCible):
        self.couleurIle = couleurIleCible

        contoursIle = self._detecterCouleur(self.couleurIle)

        if (contoursIle is not None):
            distance_x, distance_y = self._evaluerEmplacement(contoursIle)
            self.ajustements = self.alignementIle.calculerAjustement(distance_x, distance_y)

    def _detecterCouleur(self, couleur):
        if (self.couleurIle == "vert"):
            return self.detecterFormeCouleur(self.intervalleVertTable5)
        elif (self.couleurIle == "jaune"):
            return self.detecterFormeCouleur(self.intervalleJauneTable5)
        elif (self.couleurIle == "bleu"):
            return self.detecterFormeCouleur(self.intervalleBleu)
        elif (self.couleurIle == "rouge"):
            return self.detecterFormeCouleur(self.intervalleRougeTable5)

    def _evaluerEmplacement(self, contoursIle):
        position_x, position_y = self._trouverCentreForme(contoursIle)
        positionZone_x, positionZone_y = self.positionZone
        distance_x = (position_x - positionZone_x)
        distance_y = (positionZone_y - position_y)
        _, rayon = cv2.minEnclosingCircle(contoursIle)
        return distance_x, distance_y

    def detecterFormeCouleur(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        _, contoursCouleur, _ = cv2.findContours(masqueCouleur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            if ((aire < 50000) or (aire > 170000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        if (len(contoursCouleur) != 0):
            return contoursCouleur[0]
        else:
            return None

    def _trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])
        return centre_x, centre_y

    def _definirIntervallesCouleurs(self):
        self.intervalleRouge = np.array([15, 0, 75]), np.array([100, 65, 200]), "Rouge"
        self.intervalleBleu = np.array([100, 100, 0]), np.array([190, 170, 80]), "Bleu"
        self.intervalleJaune = np.array([0, 50, 50]), np.array([50, 255, 255]), "Jaune"
        self.intervalleVert = np.array([50, 120, 40]), np.array([100, 170, 80]), "Vert"
        self.intervalleVertTable5 = (np.array([0, 70, 0]), np.array([100, 200, 80])), "Vert2"
        self.intervalleRougeTable5 = (np.array([15, 0, 75]), np.array([100, 65, 200])), "Rouge2"
        self.intervalleJauneTable5 = (np.array([0, 50, 50]), np.array([50, 255, 255])), "Jaune2"

    def _afficherFeed(self):
        cv2.imshow("Image", self.imageCamera)
        cv2.waitKey(0)
