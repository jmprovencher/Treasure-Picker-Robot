from __future__ import division
from threading import Thread
import time
import cv2
from stationbase.vision.DetectionIles import DetectionIles
from stationbase.vision.DetectionTresors import DetectionTresors
from stationbase.vision.DetectionRobot import DetectionRobot
import copy
import numpy as np
from stationbase.vision.InfoTable import InfoTable


class AnalyseImageWorld(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.image = None
        self.imageCropper = None
        self.cntRobotPerdu = 0
        self.detectionPrimaireFini = False

    def run(self):
        self.stationBase.attendreFeed()
        print 'debut de la detection primaire...'
        self.detectionPrimaire()
        self.detectionPrimaireFini = True
        print 'fin de la detection primaire.'
        while 1:
            self.chargerImage()
            self.trouverRobot()
            time.sleep(0.01)

    def chargerImage(self):
        self.image = self.stationBase.getImage()
        self.recadrerImage()
        self.imageCropper = copy.deepcopy(self.image)
        self.estomperImage()

    def recadrerImage(self):
        y1, y2 = InfoTable('', self.stationBase.getNumTable()).getCrop()
        self.image = self.image[y1:y2, 0:1600]

    def estomperImage(self):
        self.image = cv2.GaussianBlur(self.image, (9, 9), 0)

    def detectionPrimaire(self):
        self.chargerImage()
        print 'trouver le robot...'
        self.trouverRobot()
        while self.stationBase.getCarte().getRobot() is None:
            print 'robot pas detecte'
            time.sleep(0.05)
            self.chargerImage()
            self.trouverRobot()
        print 'le robot est trouve.'
        self.trouverElementsCartographiques()

    def trouverElementsCartographiques(self):
        print("\nDetection des iles et tresors...")
        detectionMultipleIles = []
        detectionMultipleTresors = []

        for i in range(10):
            print 'detection: %d sur 10' % i
            self.chargerImage()
            detectionIles = DetectionIles(self.image, self.stationBase.getNumTable())
            detectionIles.detecter()
            listIles = self.eliminerContoursProcheRobot(detectionIles.getIlesIdentifiees())
            detectionMultipleIles.append(listIles)
            detectionTresors = DetectionTresors(self.image, self.stationBase.getNumTable())
            detectionTresors.detecter()
            detectionMultipleTresors.append(detectionTresors.getTresorsIdentifies())
            time.sleep(0.05)

        listIles = self.resultatPlusCommun(detectionMultipleIles)
        self.stationBase.carte.setIles(listIles)
        listTresors = self.resultatPlusCommun(detectionMultipleTresors)
        self.stationBase.carte.setTresors(listTresors)

    def resultatPlusCommun(self, detectionMultiple):
        tmpList = []
        for i in detectionMultiple:
            tmpList.append(len(i))
        return detectionMultiple[tmpList.index(max(tmpList))]

    def eliminerContoursProcheRobot(self, listIles):
        ileImpossible = []
        xRobot, yRobot = self.stationBase.getCarte().getRobot().getCentre()

        for i in range(len(listIles)):
            xIle, yIle = listIles[i].getCentre()
            if self.stationBase.getCarte().getTrajectoire().distanceAuCarre(xRobot, yRobot, xIle, yIle) <= 225:
                ileImpossible.append(i)

        if len(listIles) == len(ileImpossible):
            listIles = []
        elif not ileImpossible:
            listIles = np.delete(listIles, ileImpossible)

        return listIles

    def trouverRobot(self):
        detectionRobot = DetectionRobot(self.image, self.stationBase.getNumTable())
        detectionRobot.detecter()
        robot = detectionRobot.getRobot()
        if robot is not None:
            if self.stationBase.getCarte().getRobot() is None:
                self.stationBase.getCarte().setRobot(robot)
            elif self.deplacementPlausible(robot.getCentre()):
                self.stationBase.getCarte().setRobot(robot)
                self.cntRobotPerdu = 0
            elif self.cntRobotPerdu > 10:
                self.cntRobotPerdu = 0
                self.stationBase.getCarte().setRobot(None)
            else:
                self.cntRobotPerdu += 1
        elif self.cntRobotPerdu > 10:
                self.stationBase.getCarte().setRobot(None)
                self.cntRobotPerdu = 0
        else:
            self.cntRobotPerdu += 1

    def deplacementPlausible(self, centreRobot):
        x, y = centreRobot
        ancienX, ancienY = self.stationBase.getCarte().getRobot().getCentre()
        return self.stationBase.getCarte().getTrajectoire().distanceAuCarre(x, y, ancienX, ancienY) <= 225




