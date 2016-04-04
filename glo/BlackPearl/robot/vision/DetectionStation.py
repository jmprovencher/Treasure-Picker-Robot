from __future__ import division
import cv2
import numpy as np
import math

from robot.alignement.AlignementStation import AlignementStation

KNOWN_DISTANCE = 8
KNOWN_WIDTH = 3
FOCAL_LENGTH = 1512
RATIO_PIXEL_CM = 20

class DetectionStation(object):
    def __init__(self, image):
        self.alignementStation = AlignementStation()
        self.imageCamera = image
        self.positionZone = (810, 730)
        self.rayonZone = 20
        self._definirIntervallesCouleurs()
        self._dessinerZoneCible()
        self.ajustements = []

    def trouverAjustements(self):
        contoursCible = self._detecterFormeCouleur(self.intervalleBleuMarin)
        distance_y = self._trouverDistanceStation(contoursCible)
        distance_x = self._trouverOffsetLateral(contoursCible)
        self.ajustements = self.alignementTresor.calculerAjustement(distance_x, distance_y)
        self._dessinerInformations(contoursCible, distance_y)

    def _trouverDistanceStation(self, contoursCible):
        zoneTresor = cv2.minAreaRect(contoursCible)
        focalLength = (zoneTresor[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        print("Focal length: %d" % focalLength)

        distance_y = self._calculerDistanceCamera(KNOWN_WIDTH, FOCAL_LENGTH, zoneTresor[1][0])

        return distance_y

    def _trouverOffsetLateral(self, contoursCible):
        position_x, position_y = self._trouverCentreForme(contoursCible)
        positionZone_x, positionZone_y = self.positionZone
        distance_x = (positionZone_x - position_x) / RATIO_PIXEL_CM

        _, rayon = cv2.minEnclosingCircle(contoursCible)
        self._dessinerZoneForme((position_x, position_y), rayon)
        self._dessinerZoneCible()

        return distance_x

    def _calculerDistanceCamera(self, largeurTresor, longueurFocale, referenceLargeur):
        return (largeurTresor * longueurFocale) / referenceLargeur

    def _detecterFormeCouleur(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        cv2.imshow(couleurForme, masqueCouleur)
        cv2.waitKey(0)

        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contoursCible = self._obtenirFormeInteret(contoursCouleur)
        aire = cv2.contourArea(contoursCible)
        print ("Aire: %d" % aire)

        return contoursCible

    def _dessinerInformations(self, contoursCible, distanceStation):
        zoneTresor = cv2.minAreaRect(contoursCible)
        boiteTresor = np.int0(cv2.boxPoints(zoneTresor))
        cv2.drawContours(self.imageCamera, [boiteTresor], -1, (0, 255, 0), 2)

        cv2.putText(self.imageCamera, "%.2f cm" % (distanceStation),
                    (self.imageCamera.shape[1] - 300, self.imageCamera.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                    (0, 255, 0), 3)
        cv2.imshow("image", self.imageCamera)
        cv2.waitKey(0)

    def _trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y

    def _obtenirFormeInteret(self, contoursCouleur):
        contoursNegligeable = []
        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            print ("Aire: %d" % aire)
            if ((aire < 3000) or (aire > 7000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        return contoursCouleur[0]

    def _definirIntervallesCouleurs(self):
        self.intervalleBleuMarin = np.array([10, 180, 180]), np.array([60, 255, 255]), "Jaune"

    def _dessinerZoneCible(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def _dessinerZoneForme(self, position, rayon):
        cv2.line(self.imageCamera, self.positionZone, position, (255, 0, 0), 5)
        cv2.circle(self.imageCamera, position, int(rayon), (0, 0, 255), 2)
        print(position)
        cv2.circle(self.imageCamera, position, 10, (0, 0, 255), 2)
