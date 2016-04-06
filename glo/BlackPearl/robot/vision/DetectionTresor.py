from __future__ import division
import cv2
import numpy as np
import math
from robot.alignement.AlignementTresor import AlignementTresor

RATIOPIXEL_CM = 40


class DetectionTresor(object):
    def __init__(self, image):
        self.alignementTresor = AlignementTresor()
        self.imageCamera = image
        self.positionZone = (800, 950)
        self.rayonZone = 20
        self._definirIntervallesCouleurs()

        self.alignementTerminer = False
        self.ajustements = []

        self.calculerAjustements()

    def calculerAjustements(self):
        contoursTresor = self._detecterContoursForme(self.intervalleJauneTable5)
        if (contoursTresor is not None):
            distance_x, distance_y = self._trouverDistance(contoursTresor)
            self.ajustements = self.alignementTresor.calculerAjustement(distance_x, distance_y)

    def _trouverDistance(self, contoursTresor):
        positionZone_x, positionZone_y = self.positionZone
        position_x, position_y = self._trouverCentreForme(contoursTresor)
        distance_x = (position_x - positionZone_x)
        distance_y = (positionZone_y - position_y)
        print(distance_x, distance_y)
        return distance_x, distance_y

    def _trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y

    def _detecterContoursForme(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(masqueCouleur, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("Tresor", closing)
        cv2.waitKey(0)

        contoursTresor = []
        _, contoursCouleur, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contoursCouleur) > 0):
            contoursTresor = self._obtenirFormeInteret(contoursCouleur)
            if(contoursTresor is not None):
                aire = cv2.contourArea(contoursTresor)
                return contoursTresor
            print("Plusieurs contours detectee")
        else:
            return None

    def _obtenirFormeInteret(self, contoursCouleur):
        contoursNegligeable = []
        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            if ((aire < 1000) or (aire > 7000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)
        if (len(contoursCouleur) == 0):
            print("Aucun tresor")
            return None
        else:
            return contoursCouleur[0]

    def _definirIntervallesCouleurs(self):
        self.intervalleJaune = np.array([10, 130, 130]), np.array([60, 255, 255]), "Jaune"
        self.intervalleJauneTable5 = np.array([10, 130, 130]), np.array([60, 180, 180]), "Jaune2"
