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
        orientation = self.trouverOrientation()
        if (abs(orientation)> 1):
            ajustementOrientation = self.alignementTresor.ajusterOrientation(orientation)
            print(ajustementOrientation)
            self.ajustements.append(ajustementOrientation);

        contoursTresor = self._detecterContoursForme(self.intervalleJaune)
        if (contoursTresor is not None):
            distance_x, distance_y = self._trouverDistance(contoursTresor)
            ajustementsXY = self.alignementTresor.calculerAjustement(distance_x, distance_y)
            self.ajustements.append(ajustementsXY);

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
        _, contoursCouleur, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contoursCouleur) > 0):
            contoursTresor = self._obtenirFormeInteret(contoursCouleur)
            if (contoursTresor is not None):
                aire = cv2.contourArea(contoursTresor)
                print("Aire tresor : ", aire)
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

    def trouverOrientation(self):
        imageGrise = cv2.cvtColor(self.imageCamera, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imageGrise, (3, 3), 0)
        filtreContours = cv2.Canny(blur, 225, 250)
        _, contours, hier = cv2.findContours(filtreContours, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.imshow("Orientation", filtreContours)
        #cv2.waitKey(0)

        ligneHorizon = self.trouverLigneHorizon(contours)
        x0, y0, x1, y1 = self.trouverPointExtremeLigne(ligneHorizon)
        orientation = self.calculerOrientationHorizon(x0, y0, x1, y1)

        print("Orientation: %f" % orientation)
        #cv2.imshow("Orientation", self.imageCamera)
        #cv2.waitKey(0)
        return orientation


    def trouverLigneHorizon(self, contoursImage):
        maximum = cv2.arcLength(contoursImage[0], False)
        for cont in contoursImage:
            temp = cv2.arcLength(cont, False)
            if (temp > maximum):
                maximum = temp
                contour_max = cont
        return contour_max

    def trouverPointExtremeLigne(self, ligne):
        vx, vy, x, y = cv2.fitLine(ligne, cv2.DIST_L2, 0, 0.01, 0.01)
        pointGauche = int((-x * vy / vx) + y)
        pointDroit = int(((self.imageCamera.shape[1] - x) * vy / vx) + y)
        x0, y0 = (0, pointGauche)
        x1, y1 = (self.imageCamera.shape[1] - 1, pointDroit)
        cv2.line(self.imageCamera, (0, pointGauche), (self.imageCamera.shape[1] - 1, pointDroit), 255, 2)

        return x0, y0, x1, y1

    def calculerOrientationHorizon(self, x0, y0, x1, y1):
        mx, my = x1 - x0, y1 - y0
        roll = math.atan2(-mx, my)
        ajustement = math.degrees(roll) + 90
        return ajustement

    def _definirIntervallesCouleurs(self):
        self.intervalleJaune = np.array([0, 90, 90]), np.array([60, 255, 255]), "Jaune"

