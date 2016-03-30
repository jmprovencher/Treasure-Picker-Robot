# import the necessary packages
from __future__ import division
import sys
from threading import Thread, RLock
import time
import cv2
from elements.Ile import Ile
from elements.Tresor import Tresor
from elements.InfoRobot import InfoRobot
from stationbase.vision.DetectionIles import DetectionIles
from stationbase.vision.DetectionTresors import DetectionTresors
from stationbase.vision.DetectionRobot import DetectionRobot
import math
import copy
import numpy as np

verrou = RLock()

class AnalyseImageWorld(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.police = cv2.FONT_HERSHEY_SIMPLEX
        self.image = None
        self.imageCropper = None
        self.cntRobotPerdu = 0
        self.attendreFeed()
        self.detectionPrimaire()

    def run(self):
        while 1:
            self.chargerImage()
            self.trouverRobot()
            time.sleep(0.01)

    def attendreFeed(self):
        while self.stationBase.threadVideo.captureTable is None:
            time.sleep(0.01)

    def chargerImage(self):
        self.image = copy.deepcopy(self.stationBase.threadVideo.captureTable)
        self.recadrerImage()
        self.imageCropper = self.image
        self.estomperImage()

    def chargerImagePrimaire(self):
        self.image = self.stationBase.threadVideo.captureTable
        self.recadrerImage()
        self.imageCropper = self.image

    def recadrerImage(self):
        self.image = self.image[155:1010, 0:1600]

    def estomperImage(self):
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)
        #self.image = cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 21)

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(round(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00']))
        centre_y = int(round(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00']))

        return centre_x, centre_y

    def identifierForme(self, forme):
        contoursForme, nomForme, couleurForme = forme
        centreForme = self.trouverCentreForme(contoursForme)
        #x, y = centreForme

        if (couleurForme == ""):
            tresor = Tresor(centreForme)
            self.elementsCartographiques.append(tresor)
        else:
            ile = Ile(centreForme, couleurForme, nomForme)
            self.elementsCartographiques.append(ile)

    def detectionPrimaire(self):
        self.chargerImagePrimaire()
        self.trouverElementsCartographiques()
        self.estomperImage()
        print("\nDetection du robot...")
        self.trouverRobotInitiale()
        print 'robot trouve'
        self.eliminerContoursProcheRobot()

    def eliminerContoursProcheRobot(self):
        xDuRobotMax = self.stationBase.getPositionRobot()[0] + 50
        xDuRobotMin = self.stationBase.getPositionRobot()[0] - 50
        yDuRobotMax = self.stationBase.getPositionRobot()[1] + 50
        yDuRobotMin = self.stationBase.getPositionRobot()[1] - 50
        print 'ok!'
        eleASup = []
        for i in range(len(self.stationBase.carte.listeIles)):
            x, y = self.stationBase.carte.listeIles[i].getCentre()
            if (xDuRobotMax > x) and (xDuRobotMin < x) and (yDuRobotMax > y) and (yDuRobotMin < y):
                eleASup.append(i)
        if (len(eleASup) > 0):
            contoursCouleur = np.delete(self.stationBase.carte.listeIles, eleASup)


    def trouverElementsCartographiques(self):
        print("\nDetection des iles...")
        self.detectionIles = DetectionIles(self.image)
        self.detectionIles.detecter()
        for ile in self.detectionIles.ilesIdentifiees:
            contoursForme, nomForme, couleurForme = ile
            centreForme = self.trouverCentreForme(contoursForme)
            self.stationBase.carte.listeIles.append(Ile(centreForme, couleurForme, nomForme))

        print("\nDetection des tresors...")
        self.detectionTresors = DetectionTresors(self.image)
        self.detectionTresors.detecter()
        if len(self.detectionTresors.tresorIdentifies) > 0:
            for tresor in self.detectionTresors.tresorIdentifies:
                contoursForme, _, _ = tresor
                centreForme = self.trouverCentreForme(contoursForme)
                x, y = centreForme
                #table2 = celle noir, x < 1347
                #table1 = x < 1314
                #table1ou2 = + - 45 pour y (max y = 45)
                #en ce moment c'est sette pour la table 5
                if ((y < 30) or (y > 810)) and (x < 1347):
                    self.stationBase.carte.listeTresors.append(Tresor(centreForme))

    def trouverInfoRobot(self, formesDetectees):
        contourDroit, contourGauche = formesDetectees
        centreDroit = self.trouverCentreForme(contourDroit)
        centreGauche = self.trouverCentreForme(contourGauche)
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

        angle = angle + 90
        if angle >= 360:
            angle = angle - 360

        return (centreRobot, angle)

    def trouverRobot(self):
        print("\ndetection du robot")
        self.detectionRobot = DetectionRobot(self.image)
        self.detectionRobot.detecter()
        if (not self.detectionRobot.robotIdentifiee is None):
            centreForme, orientation = self.trouverInfoRobot(copy.deepcopy(self.detectionRobot.robotIdentifiee))
            if self.stationBase.carte.infoRobot is None:
                self.stationBase.carte.infoRobot = InfoRobot(centreForme, orientation)
                #print orientation
            elif self.deplacementPlausible(centreForme):
                self.stationBase.carte.infoRobot = InfoRobot(centreForme, orientation)
                #print orientation
                self.cntRobotPerdu = 0
            elif self.cntRobotPerdu > 25:
                self.cntRobotPerdu = 0
                self.stationBase.carte.infoRobot = None
            else:
                self.cntRobotPerdu = self.cntRobotPerdu + 1
        else:
            self.cntRobotPerdu = self.cntRobotPerdu + 1
            if self.cntRobotPerdu > 25:
                self.stationBase.carte.infoRobot = None

    def trouverRobotInitiale(self):
        robotInitialeTrouvee = False
        print 'recherche de robot initiale'
        while not robotInitialeTrouvee:
            #print("\ndetection du robot")
            self.detectionRobot = DetectionRobot(self.image)
            self.detectionRobot.detecter()
            if (not self.detectionRobot.robotIdentifiee is None):
                centreForme, orientation = self.trouverInfoRobot(copy.deepcopy(self.detectionRobot.robotIdentifiee))
                self.stationBase.carte.infoRobot = InfoRobot(centreForme, orientation)
                robotInitialeTrouvee = True
            else:
                time.sleep(0.01)
                self.chargerImage()

    def deplacementPlausible(self, centreForme):
        x, y = centreForme
        ancienX = self.stationBase.carte.infoRobot.centre_x
        ancienY = self.stationBase.carte.infoRobot.centre_y
        depX = abs(x - ancienX)
        depY = abs(y - ancienY)
        if (self.depXPlausible(depX) and self.depYPlausible(depY)):
            return True
        else:
            return False

    def depXPlausible(self, x):
        depX = self.stationBase.carte.trajectoire.grilleCellule.depPixelXACentimetre(x)
        if depX < 50:
            return True
        else:
            return False

    def depYPlausible(self, y):
        depY = self.stationBase.carte.trajectoire.grilleCellule.depPixelXACentimetre(y)
        if depY < 50:
            return True
        else:
            return False



