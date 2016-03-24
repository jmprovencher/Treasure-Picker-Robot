from __future__ import division
import cv2
import numpy as np
import math
from robot.alignement.AlignementTresor import AlignementTresor

KNOWN_DISTANCE = 14.0
KNOWN_WIDTH = 1.0
FOCAL_LENGTH = 1512
HAUTEUR_ROBOT = 12.0

class DetectionTresor(object):
    def __init__(self, image):
        self.alignementTresor = AlignementTresor()
        self.imageCamera = image
        self.positionZone = (810, 730)
        self.rayonZone = 20
        self._definirIntervallesCouleurs()
        self._dessinerZoneCible()
        self.alignementTerminer = False
        self.ajustements = []
        
        self.detecterTresor()

    def evaluerAjustements(self, offsetLateral, distanceMur):

        self.ajustements = self.alignementTresor.calculerAjustement(offsetLateral, distanceMur)


    def detecterTresor(self):
        formeTresor = self._detecterFormeCouleur(self.intervalleJaune)
        distanceMur = self.trouverDistanceMur(formeTresor)
        offsetLateral = self.trouverOffsetLateral(formeTresor)
        self.ajustements = self.evaluerAjustements(offsetLateral, distanceMur)


    def trouverOffsetLateral(self, contoursTresor):
        position_x, position_y = self._trouverCentreForme(contoursTresor)
        positionZone_x, positionZone_y = self.positionZone
        distance_x = (positionZone_x - position_x)

        _, rayon = cv2.minEnclosingCircle(contoursTresor)
        self._dessinerZoneTresor((position_x,position_y), rayon)
        self._dessinerZoneCible()

        return distance_x


    def _trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y

    def trouverDistanceMur(self, contoursTresor):
        zoneTresor = cv2.minAreaRect(contoursTresor)
        focalLength = (zoneTresor[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        print("Focal length: %d" %focalLength)

        distanceCamera = self._calculerDistanceCamera(KNOWN_WIDTH, FOCAL_LENGTH, zoneTresor[1][0])
        print("DISTANCE",distanceCamera)
        distanceMur = math.sqrt(math.pow(distanceCamera*2.54, 2) - math.pow(HAUTEUR_ROBOT*2.54, 2))




        return distanceMur

        #boiteTresor = np.int0(cv2.boxPoints(zoneTresor))
        #cv2.drawContours(self.imageCamera, [boiteTresor], -1, (0, 255, 0), 2)
        #cv2.putText(self.imageCamera, "%.2f cm" % (distance_pouce*2.54) ,(self.imageCamera.shape[1] - 300, self.imageCamera.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)
        #cv2.imshow("image", self.imageCamera)
        #cv2.waitKey(0)

    def _calculerDistanceCamera(self, knownWidth, focalLength, perWidth):
        return (knownWidth * focalLength) / perWidth

    def _detecterFormeCouleur(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        #cv2.imshow(couleurForme, masqueCouleur)
        #cv2.waitKey(0)

        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contoursTresor = self._obtenirFormeInteret(contoursCouleur)
        aire = cv2.contourArea(contoursTresor)
        print ("Aire: %d" % aire)

        return contoursTresor

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
        self.intervalleJaune = np.array([0, 50, 50]), np.array([50, 255, 255]), "Jaune"

    def _dessinerZoneCible(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def _dessinerZoneTresor(self, position, rayon):
        couleur = (0, 0, 255)
        if (self.alignementTerminer == True):
            couleur = (0, 255, 0)
        cv2.line(self.imageCamera, self.positionZone, position, (255, 0, 0), 5)
        cv2.circle(self.imageCamera, position, int(rayon), couleur, 2)
        print(position)
        cv2.circle(self.imageCamera, position, 10, (0, 0, 255), 2)