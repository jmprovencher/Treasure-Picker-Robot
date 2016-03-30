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
        #print precision
        if (precision < 1):
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
        cv2.imshow('test', masqueRobot)
        #cv2.waitKey(0)
        _, contoursRobot, hierarchy = cv2.findContours(masqueRobot.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        indiceContoursNegligeable = []
        for i in range(0, len(contoursRobot)):
            aire = cv2.contourArea(contoursRobot[i])
            aireTrou = 0
            enfant = hierarchy[0][i][2]
            if not enfant < 0:
                aireTrou = cv2.contourArea(contoursRobot[hierarchy[0][i][2]])
            if ((aire < 500) or (aire > 10000)):
                indiceContoursNegligeable.append(i)
            elif ((aireTrou < 10) or (aireTrou > 6000)):
                indiceContoursNegligeable.append(i)

        if (len(indiceContoursNegligeable) > 0):
            contoursRobot = np.delete(contoursRobot, indiceContoursNegligeable)

        self.precisionDroit = 5
        self.precisionGauche = 5
        for contoursForme in contoursRobot:
            self._trouverForme(contoursForme)

        if ((self.precisionGauche == 5) or (self.precisionDroit == 5)):
            self.robotIdentifiee = None
        else:
            self.robotIdentifiee = (self.formeDroit[0], self.formeGauche[0])

    def _definirIntervalleRobot(self):
        #self.intervalleRobot = np.array([100, 45, 5]), np.array([170, 110, 75])
        self.intervalleRobot = np.array([40, 0, 0]), np.array([190, 110, 100])

    def _definirPatronsFormes(self):
        patronRobotDroit = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        _, threshRobotDroit = cv2.threshold(patronRobotDroit, 127, 255, cv2.THRESH_BINARY)
        _, contoursRobotDroit, _ = cv2.findContours(threshRobotDroit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotDroit = contoursRobotDroit[0]

        patronRobotGauche = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        _, threshRobotGauche = cv2.threshold(patronRobotGauche, 127, 255, cv2.THRESH_BINARY)
        _, contoursRobotGauche, _ = cv2.findContours(threshRobotGauche, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotGauche = contoursRobotGauche[0]











