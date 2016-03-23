# import the necessary packages
import cv2
import numpy as np
import ConfigPath

class DetectionRobot(object):
    def __init__(self, image):
        self.imageCamera = image
        self.formesConnues = []
        self.formeAvant = None
        self.formeArriere = None
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
        #print precision

        if (precision < 0.2):
            #print (nomForme, precision)
            if (nomForme == 'Avant'):
                self.formeAvant = formeIdentifiee
            else:
                self.formeArriere = formeIdentifiee

        if ((self.formeArriere is None) or (self.formeAvant is None)):
            self.robotIdentifiee = None
        else:
            self.robotIdentifiee = (self.formeAvant[0], self.formeArriere[0])

    def _detecterForme(self):
        intervalleFonce, intervalleClair = self.intervalleRobot
        masqueRobot = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        #cv2.imshow('robot', masqueRobot)
        #cv2.waitKey(0)
        _, contoursRobot, _ = cv2.findContours(masqueRobot.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursRobot)):
            aire = cv2.contourArea(contoursRobot[contours])
            if ((aire < 200) or (aire > 1000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursRobot = np.delete(contoursRobot, contoursNegligeable)

        for contoursForme in contoursRobot:
            self._trouverForme(contoursForme)

    def _definirIntervalleRobot(self):
        self.intervalleRobot = np.array([15, 0, 75]), np.array([100, 65, 200])

    def _definirPatronsFormes(self):
        patronRobotAvant = cv2.imread(ConfigPath.Config().appendToProjectPath('images/xPattern.png'), 0)
        _, threshRobotAvant = cv2.threshold(patronRobotAvant, 127, 255, 0)
        _, contoursRobotAvant, _ = cv2.findContours(threshRobotAvant, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotAvant = contoursRobotAvant[0]
        self.formesConnues.append(self.cntRobotAvant)

        patronRobotArriere = cv2.imread(ConfigPath.Config().appendToProjectPath('images/etoilePattern.png'), 0)
        _, threshRobotArriere = cv2.threshold(patronRobotArriere, 127, 255, 0)
        _, contoursRobotArriere, _ = cv2.findContours(threshRobotArriere, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotArriere = contoursRobotArriere[0]
        self.formesConnues.append(self.cntRobotArriere)








