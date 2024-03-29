from __future__ import division
import cv2
import numpy as np
import math

from robot.alignement.AlignementStation import AlignementStation

KNOWN_DISTANCE = 6
KNOWN_WIDTH_ORANGE = 1
FOCAL_LENGTH = 1119
RATIO_PIXEL_CM = 95
MAX_AIRE_SIGNE_STATON = 60000


class DetectionStation(object):
    def __init__(self):
        self.alignementStation = AlignementStation()
        self.positionZone = (820, 730)
        self.rayonZone = 20
        self._definirIntervallesCouleurs()
        self.ajustements = None

    def trouverAjustements(self, image):
        self.imageCamera = image
        contoursCible = self.detecterFormeCouleur(self.intervalleOrange)
        if (contoursCible is not None):
            distance_y = self._trouverDistanceStation(contoursCible, KNOWN_WIDTH_ORANGE)
            distance_x = self._trouverOffsetLateral(contoursCible)
            self.ajustements = self.alignementStation.calculerAjustement(distance_x, distance_y)
        else:
            self.ajustements = None

    def _trouverDistanceStation(self, contoursCible, largeurConnue):
        zoneTresor = cv2.minAreaRect(contoursCible)
        distance_y = self._calculerDistanceCamera(largeurConnue, FOCAL_LENGTH, zoneTresor[1][0]) * 2.54

        return distance_y

    def _trouverOffsetLateral(self, contoursCible):
        position_x, position_y = self._trouverCentreForme(contoursCible)
        positionZone_x, positionZone_y = self.positionZone
        distance_x = (positionZone_x - position_x) / RATIO_PIXEL_CM

        return distance_x

    def _calculerDistanceCamera(self, largeurTresor, longueurFocale, referenceLargeur):
        return (largeurTresor * longueurFocale) / referenceLargeur

    def detecterFormeCouleur(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contoursCouleur) > 0):
            contoursCible = self._obtenirFormeInteret(contoursCouleur)
            if (contoursCible is not None):
                return contoursCible
            else:
                return None

    def _dessinerInformations(self, contoursCible, distanceStation):
        zoneTresor = cv2.minAreaRect(contoursCible)
        boiteTresor = np.int0(cv2.boxPoints(zoneTresor))
        cv2.drawContours(self.imageCamera, [boiteTresor], -1, (0, 255, 0), 2)

        cv2.putText(self.imageCamera, "%.2f cm" % (distanceStation),
                    (self.imageCamera.shape[1] - 300, self.imageCamera.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                    (0, 255, 0), 3)

    def _trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y

    def _obtenirFormeInteret(self, contoursCouleur):
        contoursNegligeable = []
        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            if ((aire < MAX_AIRE_SIGNE_STATON)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        if (contoursCouleur is not None):
            return contoursCouleur[0]
        else:
            return None

    def _definirIntervallesCouleurs(self):
        self.intervalleBleuMarin = np.array([120, 80, 40]), np.array([180, 150, 100]), "Bleu"
        self.intervalleOrange = np.array([0, 50, 140]), np.array([60, 150, 255]), "Orange"

    def _dessinerZoneCible(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def _dessinerZoneForme(self, position, rayon):
        cv2.line(self.imageCamera, self.positionZone, position, (255, 0, 0), 5)
        cv2.circle(self.imageCamera, position, int(rayon), (0, 0, 255), 2)
        print(position)
        cv2.circle(self.imageCamera, position, 10, (0, 0, 255), 2)
