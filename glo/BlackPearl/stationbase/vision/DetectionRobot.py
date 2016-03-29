# import the necessary packages
import cv2
import numpy as np
import ConfigPath
import copy

class DetectionRobot(object):
    def __init__(self, image):
        self.imageCamera = image
        self.formeDroit = None
        self.formeGauche = None
        self.precisionGauche = 5
        self.precisionDroit = 5
        self._definirIntervalleRobot()
        self._definirPatronsFormes()
        self.robotIdentifiee = None

    def detecter(self):
        self._detecterForme()

    def _trouverForme(self, contours):

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntRobotDroit, 1, 0.0), contours, 'Droit'))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntRobotGauche, 1, 0.0), contours, 'Gauche'))

        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme
        aire = cv2.contourArea(contours)
        if (precision < 0.1):
            if (nomForme == 'Droit' and (precision < self.precisionDroit)):
                #print 'form avant trouve:'
                #print precision
                self.precisionDroit = precision
                self.formeDroit = copy.deepcopy(formeIdentifiee)
            elif (nomForme == 'Gauche' and (precision < self.precisionGauche)):
                #print 'forme arriere trouve:'
                #print precision
                self.precisionGauche = precision
                self.formeGauche = copy.deepcopy(formeIdentifiee)

    def _detecterForme(self):
        self.formeGauche = None
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

        self.precisionDroit = 5
        self.precisionGauche = 5
        for contoursForme in contoursRobot:
            self._trouverForme(contoursForme)

        if ((self.precisionGauche == 5) or (self.precisionDroit == 5)):
            self.robotIdentifiee = None
        else:
            self.robotIdentifiee = (self.formeDroit[0], self.formeGauche[0])

    def _definirIntervalleRobot(self):
        self.intervalleRobot = np.array([102, 102, 0]), np.array([255, 255, 102])

    def _definirPatronsFormes(self):
        patronRobotDroit = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        _, threshRobotDroit = cv2.threshold(patronRobotDroit, 127, 255, cv2.THRESH_BINARY_INV)
        _, contoursRobotDroit, _ = cv2.findContours(threshRobotDroit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotDroit = contoursRobotDroit[0]

        patronRobotGauche = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        _, threshRobotGauche = cv2.threshold(patronRobotGauche, 127, 255, cv2.THRESH_BINARY_INV)
        _, contoursRobotGauche, _ = cv2.findContours(threshRobotGauche, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotGauche = contoursRobotGauche[0]











