# import the necessary packages
from __future__ import division
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideoStation import FeedVideoStation
from stationbase.communication.StationServeur import StationServeur
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
import time
import sys
from threading import Thread, RLock
import time
import cv2
import math
from stationbase.communication.RequeteJSON import RequeteJSON
import copy

verrou = RLock()

class StationBase(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.destination = None
        self.trajectoireReel = None
        self.trajectoirePrevue = None
        self.angleDesire = None
        self.arriver = False
        self.envoyerFichier = False
        self.commandeTermine = False
        self.attente = False
        #self.demarrerConnectionTCP()
        self.demarrerFeedVideo()
        self.carte = Carte()
        self.demarrerAnalyseImageWorld()
        self.demarrerImageVirtuelle()

    def run(self):
        self.demarerRoutine()

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoStation()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        self.threadCommunication = StationServeur(self)
        self.threadCommunication.start()

    def demarrerAnalyseImageWorld(self):
        self.threadAnalyseImageWorld = AnalyseImageWorld(self)
        self.threadAnalyseImageWorld.start()

    def demarrerImageVirtuelle(self):
        self.threadImageVirtuelle = ImageVirtuelle(self)
        self.threadImageVirtuelle.start()

    def demarerRoutine(self):
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.etapeStation()
        time.sleep(100000)

    def identifierDestination(self, etape):
        if (etape == 'RECHARGE'):
            self.destination = self.carte.stationRecharge.getCentre()

    def etapeStation(self):
        print '\n--------------------------------------------------'
        print 'Aller a la station de recharge'
        print '--------------------------------------------------'
        self.identifierDestination('RECHARGE')
        self.trouverTrajectoirePrevu()
        while len(self.trajectoireReel) > 1:
            self.orienter()
            self.deplacer()
        self.angleDesire = 90
        self.orienter()
        print '\n--------------------------------------------------'
        print 'Arriver a la station de recharge!'
        print '--------------------------------------------------'
        self.allignement("allignementStation")
        print '\n--------------------------------------------------'
        print 'Recharge termine'
        print '--------------------------------------------------'

    def trouverTrajectoirePrevu(self):
        while 1:
            if (not self.carte.infoRobot is None):
                self.trajectoirePrevue = self.carte.trajectoire.trouverTrajet(self.getPositionRobot(), self.destination)
                self.trajectoireReel = copy.deepcopy(self.trajectoirePrevue)
                break
            time.sleep(0.01)

    def trouverDeplacementOrientation(self):
        if self.angleDesire is None:
            arriver = self.trajectoireReel[-2]
            debut = self.getPositionRobot()
            self.angleDesire = self.trouverOrientationDesire(debut, arriver)
        angleRobot = self.getOrientationRobot()
        depDegre = angleRobot - self.angleDesire
        if depDegre < -180:
            depDegre = depDegre + 360
        elif depDegre > 180:
            depDegre = depDegre - 360

        return depDegre

    def getPositionRobot(self):
        while 1:
            if (not self.carte.infoRobot is None):
                return self.carte.infoRobot.getCentre()
            time.sleep(0.01)

    def getOrientationRobot(self):
        while 1:
            if (not self.carte.infoRobot is None):
                return self.carte.infoRobot.orientation
            time.sleep(0.01)


    def trouverOrientationDesire(self, debut, arriver):
        deltaX = arriver[0]-debut[0]
        deltaY = -1*(arriver[1]-debut[1])
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

        return angle

    def orienter(self):
        while 1:
            angle = self.trouverDeplacementOrientation()
            if angle <= 3 and angle >= -3:
                break
            myRequest = RequeteJSON("rotate", angle)
            self.envoyerFichier = True
            self.attendreRobot()
        self.angleDesire = None

    def attendreRobot(self):
        self.attente = True
        while not self.commandeTermine:
            time.sleep(0.01)
        self.commandeTermine = False

    def distanceADestinationAuCarre(self, x, y, destX, destY):
        distanceX = destX - x
        distanceY = destY - y
        distanceX = self.carte.trajectoire.grilleCellule.depPixelXACentimetre(distanceX)
        distanceY = self.carte.trajectoire.grilleCellule.depPixelYACentimetre(distanceY)
        distanceCarre = distanceX**2 + distanceY**2
        return distanceCarre

    def distanceADestination(self, x, y, destX, destY):
        distancePixX = destX - x
        distancePixY = destY - y
        distanceX = self.carte.trajectoire.grilleCellule.depPixelXACentimetre(distancePixX)
        distanceY = self.carte.trajectoire.grilleCellule.depPixelYACentimetre(distancePixY)
        distance = int(round(math.sqrt(distanceX**2 + distanceY**2)))
        return distance

    def deplacer(self):
        arriver = self.trajectoireReel[-2]
        debut = self.getPositionRobot()
        dep = self.distanceADestination(debut[0], debut[1], arriver[0], arriver[1])
        RequeteJSON("forward", dep)
        self.envoyerFichier = True
        self.attendreRobot()
        debut = self.getPositionRobot()
        dep = self.distanceADestinationAuCarre(debut[0], debut[1], arriver[0], arriver[1])
        if dep <= 25:
            print '\netape de complete'
            self.trajectoireReel.pop(-1)

    def allignement(self, type):
        RequeteJSON(type, 0)
        self.envoyerFichier = True
        self.attendreRobot()




