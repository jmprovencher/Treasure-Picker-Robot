# import the necessary packages
import cv2
import numpy as np
import ConfigPath
'''
class DetectionRobot(object):
    def __init__(self, image):
        self.imageCamera = image
        self.formesConnues = []
        self.robotIdentifiee = None
        self._definirIntervallesCouleurs()
        self._definirPatronsFormes()

    def detecter(self):
        self._detecterFormeCouleur(self.intervalleRobot)

    def _trouverForme(self, contours, couleur):

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntRobot, 1, 0.0), contours, "Robot"))

        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme, couleur

        robotExiste = False

        if (precision < 0.5):
            #print (nomForme, couleur, precision)
            self.robotIdentifiee = formeIdentifiee
            robotExiste = True
            #print "Robot trouve"

        if (robotExiste == False):
            self.robotIdentifiee = None

    def _detecterFormeCouleur(self, intervalleCouleur):

        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueRouge = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursRouge, _ = cv2.findContours(masqueRouge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursRouge)):
            aire = cv2.contourArea(contoursRouge[contours])
            if ((aire < 1000) or (aire > 6000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursRouge = np.delete(contoursRouge, contoursNegligeable)
        #a checker avec table si ca plante
        if len(contoursRouge) < 10:
            for contoursForme in contoursRouge:
                self._trouverForme(contoursForme, couleurForme)

    def _definirIntervallesCouleurs(self):
        self.intervalleRobot = np.array([15, 0, 75]), np.array([100, 65, 200]),"Rose"

    def _definirPatronsFormes(self):
        patronRobot = cv2.imread(ConfigPath.Config().appendToProjectPath('images/robotPasEleve.png'), 0)
        precision, threshRobot = cv2.threshold(patronRobot, 127, 255, 0)

        _, contoursRobot, _ = cv2.findContours(threshRobot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobot = contoursRobot[0]

        self.formesConnues.append(self.cntRobot)

'''
class DetectionRobot(object):
    def __init__(self, image):
        self.imageCamera = image
        self.formeAvant = None
        self.formeArriere = None
        self._definirIntervalleRouge()
        self._definirPatronsFormes()
        self.robotIdentifiee = None

    def detecter(self):
        self._detecterForme()

    def _trouverForme(self, contours):

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntTriangle, 1, 0.0), contours, 'Avant'))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCercle, 1, 0.0), contours, 'Arriere'))

        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme

        if (precision < 0.5):
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
        intervalleFonce, intervalleClair, couleurForme = self.intervalleRouge
        masqueRouge = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursRouge, _ = cv2.findContours(masqueRouge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursRouge)):
            aire = cv2.contourArea(contoursRouge[contours])
            if ((aire < 100) or (aire > 3000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursRouge = np.delete(contoursRouge, contoursNegligeable)

        for contoursForme in contoursRouge:
            self._trouverForme(contoursForme)

    def _definirIntervalleRouge(self):
        self.intervalleRouge = np.array([15, 0, 75]), np.array([100, 65, 200]),'Rouge'

    def _definirPatronsFormes(self):
        patronRobotAvant = cv2.imread(ConfigPath.Config().appendToProjectPath('images/robotAvantPasEleve.png'), 0)
        _, threshRobotAvant = cv2.threshold(patronRobotAvant, 127, 255, 0)
        _, contoursRobotAvant, _ = cv2.findContours(threshRobotAvant, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotAvant = contoursRobotAvant[0]
        self.formesConnues.append(self.cntRobotAvant)

        patronRobotArriere = cv2.imread(ConfigPath.Config().appendToProjectPath('images/robotArrierePasEleve.png'), 0)
        _, threshRobotArriere = cv2.threshold(patronRobotArriere, 127, 255, 0)
        _, contoursRobotArriere, _ = cv2.findContours(threshRobotArriere, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotArriere = contoursRobotArriere[0]
        self.formesConnues.append(self.cntRobotArriere)








