# import the necessary packages
import cv2
import numpy as np
import ConfigPath
import copy

class DetectionRobot(object):
    def __init__(self, image):
        self.imageCamera = image
        self.formeAvant = None
        self.formeArriere = None
        self.precisionArriere = 5
        self.precisionAvant = 5
        self._definirIntervalleRobot()
        self._definirPatronsFormes()
        self.robotIdentifiee = None

    def detecter(self):
        self._detecterForme()

    def _trouverForme(self, contours):

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntRobotAvant, 1, 0.0), contours, 'Avant'))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntRobotArriere, 1, 0.0), contours, 'Arriere'))

        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme
        aire = cv2.contourArea(contours)
        if (precision < 0.03):
            if (nomForme == 'Avant' and (precision < self.precisionAvant)):
                #print 'form avant trouve:'
                #print precision
                self.precisionAvant = precision
                self.formeAvant = copy.deepcopy(formeIdentifiee)
            elif (nomForme == 'Arriere' and (precision < self.precisionArriere)):
                #print 'forme arriere trouve:'
                #print precision
                self.precisionArriere = precision
                self.formeArriere = copy.deepcopy(formeIdentifiee)

    def _detecterForme(self):
        self.formeArriere = None
        intervalleFonce, intervalleClair = self.intervalleRobot
        masqueRobot = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        #cv2.imshow('test', masqueRobot)
        #cv2.waitKey(0)
        _, contoursRobot, _ = cv2.findContours(masqueRobot.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursRobot)):
            aire = cv2.contourArea(contoursRobot[contours])
            if ((aire < 1000) or (aire > 6000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursRobot = np.delete(contoursRobot, contoursNegligeable)

        self.precisionAvant = 5
        self.precisionArriere = 5
        for contoursForme in contoursRobot:
            self._trouverForme(contoursForme)

        if ((self.precisionArriere == 5) or (self.precisionAvant == 5)):
            self.robotIdentifiee = None
        else:
            self.robotIdentifiee = (self.formeAvant[0], self.formeArriere[0])

    def _definirIntervalleRobot(self):
        self.intervalleRobot = np.array([25, 0, 50]), np.array([150, 100, 200])

    def _definirPatronsFormes(self):
        patronRobotAvant = cv2.imread(ConfigPath.Config().appendToProjectPath('images/xPattern.png'), 0)
        _, threshRobotAvant = cv2.threshold(patronRobotAvant, 127, 255, cv2.THRESH_BINARY_INV)
        #cv2.imshow('test', threshRobotAvant)
        #cv2.waitKey(0)
        _, contoursRobotAvant, _ = cv2.findContours(threshRobotAvant, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotAvant = contoursRobotAvant[0]

        patronRobotArriere = cv2.imread(ConfigPath.Config().appendToProjectPath('images/etoilePattern.png'), 0)
        _, threshRobotArriere = cv2.threshold(patronRobotArriere, 127, 255, cv2.THRESH_BINARY_INV)
        _, contoursRobotArriere, _ = cv2.findContours(threshRobotArriere, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotArriere = contoursRobotArriere[0]











