from __future__ import division
import cv2
import numpy as np
import math
from robot.alignement.AlignementIle import AlignementIle


class DetectionIle(object):
    def __init__(self, image, couleurIleCible):
        self.alignementIle = AlignementIle()
        self.alignementTerminer = False
        self.imageCamera = image
        self.couleurIle = couleurIleCible
        self.ajustements = []

        self.positionZone = (800, 850)
        self.rayonZone = 100

        self._definirIntervallesCouleurs()
        self.dessinerZoneCible()
        self.detecterIle()

    def detecterIle(self):
        if (self.couleurIle == "vert"):
            self._detecterFormeCouleur(self.intervalleVert)
        elif (self.couleurIle == "jaune"):
            self._detecterFormeCouleur(self.intervalleJaune)
        elif (self.couleurIle == "bleu"):
            self._detecterFormeCouleur(self.intervalleBleu)
        elif (self.couleurIle == "rouge"):
            self._detecterFormeCouleur(self.intervalleRouge)

    def evaluerEmplacement(self, contoursIle):
        position_x, position_y = self._trouverCentreForme(contoursIle)
        positionZone_x, positionZone_y = self.positionZone
        distance_x = (positionZone_x - position_x)
        distance_y = (positionZone_y - position_y)
        distance = math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))
        _, rayon = cv2.minEnclosingCircle(contoursIle)

        self.dessinerZoneIle((position_x, position_y), rayon)

        ######### A retravailler
        if (distance <= self.rayonZone):
            self.alignementTerminer = True
            self.alignementIle.completerDepot()
            self.ajustements = []
        else:
            self.ajustements = self.alignementIle.calculerAjustement(distance_x, distance_y)

        self._afficherFeed()

    def dessinerZoneCible(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def dessinerZoneIle(self, position, rayon):
        couleur = (0, 0, 255)
        if (self.alignementTerminer == True):
            couleur = (0, 255, 0)
        cv2.line(self.imageCamera, self.positionZone, position, (255, 0, 0), 5)
        cv2.circle(self.imageCamera, position, int(rayon), couleur, 2)
        print(position)
        cv2.circle(self.imageCamera, position, 10, (0, 0, 255), 2)

    def _detecterFormeCouleur(self, intervalleCouleur):
        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        #cv2.imshow(couleurForme, masqueCouleur)
        #cv2.waitKey(0)

        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            print ("Aire: %d" % aire)
            if ((aire < 50000) or (aire > 150000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        if (len(contoursCouleur) != 0):
            print("EvaluerPosition is called")
            self.evaluerEmplacement(contoursCouleur[0])

    def _trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])
        return centre_x, centre_y

    def _definirIntervallesCouleurs(self):
        self.intervalleRouge = np.array([15, 0, 75]), np.array([100, 65, 200]), "Rouge"
        self.intervalleOrange = np.array([50, 100, 100]), np.array([80, 120, 180]), "Orange"
        self.intervalleBleu = np.array([100, 100, 0]), np.array([190, 170, 80]), "Bleu"
        self.intervalleJaune = np.array([0, 50, 50]), np.array([50, 255, 255]), "Jaune"
        self.intervalleVert = np.array([50, 120, 40]), np.array([100, 170, 80]), "Vert"

    def _afficherFeed(self):
        cv2.imshow("Image", self.imageCamera)