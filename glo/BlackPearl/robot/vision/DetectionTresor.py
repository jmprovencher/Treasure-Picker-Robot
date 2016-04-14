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
        self.ajustements = None
        #self._dessinerZoneCible()

    def calculerAjustements(self):
        #self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('horizon.jpg'))
        contoursTresor = self._detecterContoursForme(self.intervalleJaune)

        if (contoursTresor is not None):
            distance_x, distance_y = self._trouverDistance(contoursTresor)
            self.ajustements= self.alignementTresor.calculerAjustement(distance_x, distance_y)
            print("Ajustement alignement tresor calculer")
        else:
            self.ajustements = None

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
        closing = cv2.morphologyEx(masqueCouleur.copy(), cv2.MORPH_CLOSE, kernel)
        _, contoursCouleur, _ = cv2.findContours(closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.imshow("Tresor", closing)
        #cv2.waitKey(0)

        if (len(contoursCouleur) > 0):
            print("Va filtrer %d forme: " %len(contoursCouleur))
            contoursTresor = self._obtenirFormeInteret(contoursCouleur)

            if (contoursTresor is not None):
                return contoursTresor
            else:
                print("Plusieurs contours detectee")
                return None
        else:
            print("FUCKED UP")
            return None

    def _obtenirFormeInteret(self, contoursCouleur):
        contoursNegligeable = []

        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            #print("Aire tresor: %f" %aire)

            if ((aire < 3000) or (aire > 9000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)

        print("Nombre de forme apres: %d" %len(contoursCouleur))

        #cv2.imshow("Tresor", self.imageCamera)
        #cv2.waitKey(0)

        if (len(contoursCouleur) == 0):
            print("Aucun tresor")
            return None
        else:
            contoursCouleur.sort()
            index = len(contoursCouleur)
            return contoursCouleur[index-1]

    def _dessinerZoneCible(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def _definirIntervallesCouleurs(self):
        #self.intervalleJaune = np.array([0, 0, 0]), np.array([255, 255, 255]), "Jaune"
        #self.intervalleJaune = np.array([20, 90, 90]), np.array([80, 255, 255]), "Jaune"
        self.intervalleJaune = np.array([0, 90, 90]), np.array([80, 255, 255]), "Jaune"