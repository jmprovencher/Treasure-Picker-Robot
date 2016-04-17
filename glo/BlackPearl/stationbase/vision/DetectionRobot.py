from __future__ import division
import cv2
import numpy as np
import ConfigPath
import copy
import math
from stationbase.vision.InfoTable import InfoTable
from stationbase.vision.Detection import Detection
from elements.Robot import Robot

MIN_AIRE_CONTOUR = 500
MAX_AIRE_CONTOUR = 10000
MAX_PRECISION = 0.5
MIN_AIRE_TROU = 10
MAX_AIRE_TROU = 2000

class DetectionRobot(Detection):
    def __init__(self, image, numeroTable):
        Detection.__init__(self, image, numeroTable)
        self.robotIdentifiee = None
        self._definirPatronsFormes()

    def detecter(self):
        contoursRobot, hierarchie = self.trouverContoursRobot()
        contoursRobot = self.eleminerCoutoursNegligeable(contoursRobot, hierarchie)
        self.trouverRobot(contoursRobot)
            
    def trouverContoursRobot(self):
        intervalleFonce, intervalleClair = InfoTable('Robot', self.numeroTable).getIntervalle()
        masqueRobot = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursRobot, hierarchie = cv2.findContours(masqueRobot.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        return contoursRobot, hierarchie
    
    def eleminerCoutoursNegligeable(self, contoursRobot, hierarchie):
        contoursNegligeables = []
        for i in range(len(contoursRobot)):
            aireContour = cv2.contourArea(contoursRobot[i])
            indiceContourTrou = hierarchie[0][i][2]
            
            if indiceContourTrou >= 0:  # Signifie que le contour possede un trou
                aireTrouContour = cv2.contourArea(contoursRobot[indiceContourTrou])
            else:
                aireTrouContour = 0
                
            if (aireContour < MIN_AIRE_CONTOUR) or (aireContour > MAX_AIRE_CONTOUR):
                contoursNegligeables.append(i)
            elif (aireTrouContour < MIN_AIRE_TROU) or (aireTrouContour > MAX_AIRE_TROU):
                contoursNegligeables.append(i)
                
        if len(contoursRobot) == len(contoursNegligeables):
            contoursRobot = []
        elif contoursNegligeables:
            contoursRobot = np.delete(contoursRobot, contoursNegligeables)

        return contoursRobot

    def trouverRobot(self, contoursRobot):
        precisionDroite = 1000
        precisionGauche = 1000
        contourDroit = None
        contourGauche = None
        
        for contour in contoursRobot:
            resultatsMatch = []
            resultatsMatch.append((cv2.matchShapes(contour, self.cntRobotDroit, 1, 0.0), contour, 'Droite'))
            resultatsMatch.append((cv2.matchShapes(contour, self.cntRobotGauche, 1, 0.0), contour, 'Gauche'))
            meilleurMatch = min(resultatsMatch)
            precision, contour, position = meilleurMatch

            if precision < MAX_PRECISION:
                if (position == 'Droite') and (precision < precisionDroite):
                    precisionDroite = precision
                    contourDroit = copy.deepcopy(contour)
                elif (position == 'Gauche') and (precision < precisionGauche):
                    precisionGauche = precision
                    contourGauche = copy.deepcopy(contour)
                    
        if (contourDroit is None) or (contourGauche is None):
            self.robotIdentifiee = None
        else:
            centre, orientation = self.trouverInfoRobot(contourGauche, contourDroit)
            self.robotIdentifiee = Robot(centre, orientation)

    def trouverInfoRobot(self, contourGauche, contourDroit):
        centreGauche = self.trouverCentre(contourGauche)
        centreDroit = self.trouverCentre(contourDroit)
        centreRobot = (int(round((centreDroit[0]+centreGauche[0])/2)), int(round((centreDroit[1]+centreGauche[1])/2)))
        deltaX = centreDroit[0]-centreGauche[0]
        deltaY = -1*(centreDroit[1]-centreGauche[1])
        if not deltaX == 0:
            pente = deltaY/deltaX

        if deltaY == 0 and deltaX < 0:
            angle = 180
        elif deltaY == 0 and deltaX > 0:
            angle = 0
        elif deltaX == 0 and deltaY > 0:
            angle = 90
        elif deltaX == 0 and deltaY < 0:
            angle = 270
        elif deltaX > 0 and deltaY > 0:
            angle = int(round(math.degrees(math.atan(pente))))
        elif deltaX > 0 and deltaY < 0:
            angle = 360 + int(round(math.degrees(math.atan(pente))))
        elif deltaX < 0:
            angle = 180 + int(round(math.degrees(math.atan(pente))))

        angle += 90
        if angle >= 360:
            angle -= 360

        return centreRobot, angle

    def getRobot(self):
        return self.robotIdentifiee

    def _definirPatronsFormes(self):
        patronRobotDroit = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        _, threshRobotDroit = cv2.threshold(patronRobotDroit, 127, 255, cv2.THRESH_BINARY)
        _, contoursRobotDroit, _ = cv2.findContours(threshRobotDroit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotDroit = contoursRobotDroit[0]

        patronRobotGauche = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        _, threshRobotGauche = cv2.threshold(patronRobotGauche, 127, 255, cv2.THRESH_BINARY)
        _, contoursRobotGauche, _ = cv2.findContours(threshRobotGauche, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntRobotGauche = contoursRobotGauche[0]











