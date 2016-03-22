# import the necessary packages
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

verrou = RLock()

class AnalyseImageWorld(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.police = cv2.FONT_HERSHEY_SIMPLEX
        self.image = None
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
        self.image = self.stationBase.threadVideo.captureTable
        self.recadrerImage()
        self.estomperImage()

    def recadrerImage(self):
        self.image = self.image[155:1010, 0:1600]

    def estomperImage(self):
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(round(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00']))
        centre_y = int(round(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00']))

        return centre_x, centre_y

    def identifierForme(self, forme):
        contoursForme, nomForme, couleurForme = forme
        centreForme = self.trouverCentreForme(contoursForme)

        if (couleurForme == ""):
            tresor = Tresor(centreForme)
            self.elementsCartographiques.append(tresor)
        else:
            ile = Ile(centreForme, couleurForme, nomForme)
            self.elementsCartographiques.append(ile)

    def detectionPrimaire(self):
        self.chargerImage()
        self.trouverElementsCartographiques()

    def trouverElementsCartographiques(self):
        print("\ndetection des iles")
        self.detectionIles = DetectionIles(self.image)
        self.detectionIles.detecter()
        for ile in self.detectionIles.ilesIdentifiees:
            contoursForme, nomForme, couleurForme = ile
            centreForme = self.trouverCentreForme(contoursForme)
            with verrou:
                self.stationBase.carte.listeIles.append(Ile(centreForme, couleurForme, nomForme))

        print("\ndetection des tresors")
        self.detectionTresors = DetectionTresors(self.image)
        self.detectionTresors.detecter()
        for tresor in self.detectionTresors.tresorIdentifies:
            contoursForme, _, _ = tresor
            centreForme = self.trouverCentreForme(contoursForme)
            with verrou:
                self.stationBase.carte.listeTresors.append(Tresor(centreForme))

        self.trouverRobot()

    def trouverInfoRobot(self, formesDetectees):
        contourAvant, contourArriere = formesDetectees
        centreAvant = self.trouverCentreForme(contourAvant)
        centrearriere = self.trouverCentreForme(contourArriere)
        centreRobot = ((centreAvant[0]+centrearriere[0])/2, (centreAvant[1]+centrearriere[1])/2)
        deltaX = centreAvant[0]-centrearriere[0]
        deltaY = centreAvant[1]-centrearriere[1]
        if not deltaX == 0:
            pente = deltaY/deltaX

        if deltaX < 0:
            angle = 180+math.atan(pente)
        elif deltaY <= 0 and deltaX > 0:
            angle = math.atan(pente)
        elif deltaY > 0 and deltaX > 0:
            angle = 360+math.atan(pente)
        elif deltaX == 0 and deltaY > 0:
            angle = 270
        elif deltaX == 0 and deltaY < 0:
            angle = 90

        int(round(math.degrees(angle)))

        return (centreRobot, angle)

    def trouverRobot(self):
        #print("\ndetection du robot")
        self.detectionRobot = DetectionRobot(self.image)
        self.detectionRobot.detecter()
        if (not self.detectionRobot.robotIdentifiee is None):
            centreForme, orientation = self.trouverInfoRobot(self.detectionRobot.robotIdentifiee)
            with verrou:
                self.stationBase.carte.infoRobot = InfoRobot(centreForme, orientation)



