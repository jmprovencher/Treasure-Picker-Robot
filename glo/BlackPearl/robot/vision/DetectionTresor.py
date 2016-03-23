from __future__ import division
import cv2
import numpy as np
import math

KNOWN_DISTANCE = 8
KNOWN_WIDTH = 1.0
FOCAL_LENGTH = 864

class DetectionTresor(object):
    def __init__(self, image):
        self.imageCamera = image
        self.positionZone = (810, 730)
        self.rayonZone = 20
        self._definirIntervallesCouleurs()
        self.dessinerZoneCible()
        self.alignementTerminer = False
        self.ajustements = []
        
        self.detecterTresor()

    def evaluerPosition(self, contoursIle):
        position_x, position_y = self.trouverCentreForme(contoursIle)
        positionZone_x, positionZone_y = self.positionZone
        distance_x = (positionZone_x - position_x)
        distance_y = (positionZone_y - position_y)
        distance = math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))
        _, rayon = cv2.minEnclosingCircle(contoursIle)

        ######### A retravailler
        if (distance <= self.rayonZone):
            self.alignementTerminer = True
            self.dessinerZoneTresor((position_x, position_y), rayon)
            # self.alignementIle.completerDepot()
            self.ajustements = []
        else:
            self.dessinerZoneTresor((position_x, position_y), rayon)
            # self.ajustements = self.alignementIle.calculerAjustement(distance_x, distance_y)

        cv2.imshow("Detection Tresor", self.imageCamera)
        cv2.waitKey(0)

    def dessinerZoneCible(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def dessinerZoneTresor(self, position, rayon):
        couleur = (0, 0, 255)
        if (self.alignementTerminer == True):
            couleur = (0, 255, 0)
        cv2.line(self.imageCamera, self.positionZone, position, (255, 0, 0), 5)
        cv2.circle(self.imageCamera, position, int(rayon), couleur, 2)
        print(position)
        cv2.circle(self.imageCamera, position, 10, (0, 0, 255), 2)

    def trouverDistance(self, contoursTresor):
        zoneTresor = cv2.minAreaRect(contoursTresor)
        #focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        #print("Focal length: %d" %focalLength)
        inches = self._calculerDistanceCamera(KNOWN_WIDTH, FOCAL_LENGTH, zoneTresor[1][0])

        boiteTresor = np.int0(cv2.boxPoints(zoneTresor))
        cv2.drawContours(self.imageCamera, [boiteTresor], -1, (0, 255, 0), 2)
        cv2.putText(self.imageCamera, "%.2f cm" % (inches*2.54) ,(self.imageCamera.shape[1] - 300, self.imageCamera.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)
        cv2.imshow("image", self.imageCamera)
        cv2.waitKey(0)

    def detecterTresor(self):
        self._detecterFormeCouleur(self.intervalleJaune)

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y

    def _calculerDistanceCamera(self, knownWidth, focalLength, perWidth):
        return (knownWidth * focalLength) / perWidth

    def _detecterFormeCouleur(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        # cv2.imshow(couleurForme, masqueCouleur)
        # cv2.waitKey(0)

        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            print ("Aire: %d" % aire)
            if ((aire < 3000) or (aire > 7000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        if (len(contoursCouleur) != 0):
            self.trouverDistance(contoursCouleur[0])
            #self.evaluerPosition(contoursCouleur[0])

    def _definirIntervallesCouleurs(self):
        self.intervalleJaune = np.array([0, 50, 50]), np.array([50, 255, 255]), "Jaune"
