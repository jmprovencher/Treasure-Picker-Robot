# import the necessary packages
import cv2
import numpy as np
import ConfigPath


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

        if (precision < 0.5):
            #print (nomForme, couleur, precision)
            self.robotIdentifiee = formeIdentifiee
            #print "Robot trouve"

    def _detecterFormeCouleur(self, intervalleCouleur):

        intervalleFonce, intervalleClair, couleurForme = intervalleCouleur
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursNegligeable = []

        for contours in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[contours])
            if ((aire < 1000) or (aire > 6000)):
                contoursNegligeable.append(contours)

        if (len(contoursNegligeable) > 0):
            contoursCouleur = np.delete(contoursCouleur, contoursNegligeable)
        #a checker avec table si ca plante
        if len(contoursCouleur) < 10:
            for contoursForme in contoursCouleur:
                self._trouverForme(contoursForme, couleurForme)

    def _definirIntervallesCouleurs(self):
        self.intervalleRobot = np.array([15, 0, 75]), np.array([100, 65, 200]),"Rose"

    def _definirPatronsFormes(self):
        patronRobot = cv2.imread(ConfigPath.Config().appendToProjectPath('images/robotPasEleve.png'), 0)
        precision, threshRobot = cv2.threshold(patronRobot, 127, 255, 0)

        _, contoursRobot, _ = cv2.findContours(threshRobot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobot = contoursRobot[0]

        self.formesConnues.append(self.cntRobot)




