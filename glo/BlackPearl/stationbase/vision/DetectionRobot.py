import cv2
import numpy as np
import ConfigPath
import copy

class DetectionRobot(object):
    def __init__(self, image):
        self.imageCamera = image
        self.robotIdentifiee = None
        self._definirPatronsFormes()

    def detecter(self):
        contoursRobot, hierarchy = self.trouverContoursRobot()
        contoursRobot = self.eleminerCoutoursNegligeable(contoursRobot, hierarchy)
        self.trouverRobot(contoursRobot)
            
    def trouverContoursRobot(self):
        intervalleFonce, intervalleClair = (np.array([30, 5, 140]), np.array([145, 140, 245]))
        masqueRobot = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursRobot, hierarchy = cv2.findContours(masqueRobot.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        return (contoursRobot, hierarchy)
    
    def eleminerCoutoursNegligeable(self, contoursRobot, hierarchy):
        contoursNegligeables = []
        
        for i in range(len(contoursRobot)):
            aireContour = cv2.contourArea(contoursRobot[i])
            indiceContourTrou = hierarchy[0][i][2]
            
            if indiceContourTrou >= 0:  # Signifie que le contour possede un trou
                aireTrouContour = cv2.contourArea(contoursRobot[indiceContourTrou])
            else:
                aireTrouContour = 0
                
            if ((aireContour < 500) or (aireContour > 10000)):
                contoursNegligeables.append(i)
            elif ((aireTrouContour < 10) or (aireTrouContour > 6000)):
                contoursNegligeables.append(i)
                
        if len(contoursRobot) == len(contoursNegligeables):
            contoursRobot = []
        elif (len(contoursNegligeables) > 0):
            contoursRobot = np.delete(contoursRobot, contoursNegligeables)
            
        return contoursRobot

    def trouverRobot(self, contoursRobot):
        precisionDroit = 1000
        precisionGauche = 1000
        contourDroit = None
        contourGauche = None
        
        for contour in contoursRobot:
            resultatsMatch = []
            resultatsMatch.append((cv2.matchShapes(contour, self.cntRobotDroit, 1, 0.0), contour, 'Droit'))
            resultatsMatch.append((cv2.matchShapes(contour, self.cntRobotGauche, 1, 0.0), contour, 'Gauche'))
            meilleurMatch = min(resultatsMatch)
            precision, contour, nomForme = meilleurMatch

            if (precision < 0.5):
                if (nomForme == 'Droit' and (precision < precisionDroit)):
                    precisionDroit = precision
                    contourDroit = copy.deepcopy(contour)
                elif (nomForme == 'Gauche' and (precision < precisionGauche)):
                    precisionGauche = precision
                    contourGauche = copy.deepcopy(contour)
                    
        if (contourDroit is None) or (contourGauche is None):
            self.robotIdentifiee = None
        else:
            self.robotIdentifiee = (contourGauche, contourDroit)

    def _definirPatronsFormes(self):
        patronRobotDroit = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        _, threshRobotDroit = cv2.threshold(patronRobotDroit, 127, 255, cv2.THRESH_BINARY)
        _, contoursRobotDroit, _ = cv2.findContours(threshRobotDroit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotDroit = contoursRobotDroit[0]

        patronRobotGauche = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        _, threshRobotGauche = cv2.threshold(patronRobotGauche, 127, 255, cv2.THRESH_BINARY)
        _, contoursRobotGauche, _ = cv2.findContours(threshRobotGauche, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotGauche = contoursRobotGauche[0]











