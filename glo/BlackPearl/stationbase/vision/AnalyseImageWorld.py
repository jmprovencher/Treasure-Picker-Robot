from __future__ import division
from threading import Thread
import time
import cv2
from stationbase.vision.DetectionIles import DetectionIles
from stationbase.vision.DetectionTresors import DetectionTresors
from stationbase.vision.DetectionRobot import DetectionRobot
import copy
import numpy as np


class AnalyseImageWorld(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.image = None
        self.imageCropper = None
        self.cntRobotPerdu = 0

    def run(self):
        self.attendreFeed()
        self.detectionPrimaire()
        while 1:
            self.chargerImage()
            self.trouverRobot()
            time.sleep(0.01)

    def attendreFeed(self):
        self.stationBase.attendreFeed()

    def chargerImage(self):
        self.image = self.stationBase.getImage()
        self.recadrerImage()
        self.imageCropper = copy.deepcopy(self.image)
        self.estomperImage()

    def recadrerImage(self):
        self.image = self.image[155:1010, 0:1600]

    def estomperImage(self):
        self.image = cv2.GaussianBlur(self.image, (9, 9), 0)

    def detectionPrimaire(self):
        self.trouverElementsCartographiques()
        self.trouverRobot()
        while self.getRobot() is None:
            time.sleep(0.05)
            self.chargerImage()
            self.trouverRobot()
        self.eliminerContoursProcheRobot()

    def trouverElementsCartographiques(self):
        print("\nDetection des iles et tresors...")
        detectionMultipleIles = []
        detectionMultipleTresors = []

        for i in range(10):
            self.chargerImage()
            detectionIles = DetectionIles(self.image, self.numeroTable)
            detectionIles.detecter()
            detectionMultipleIles.append(detectionIles.getIlesIdentifiees())
            detectionTresors = DetectionTresors(self.image, self.numeroTable)
            detectionTresors.detecter()
            detectionMultipleTresors.append(detectionTresors.getTresorsIdentifies())
            time.sleep(0.05)

        listIles = self.resultatPlusCommun(detectionMultipleIles)
        self.stationBase.getCarte().setIles(listIles)
        listTresors = self.resultatPlusCommun(detectionMultipleTresors)
        self.stationBase.getCarte().setTresors(listTresors)

    def resultatPlusCommun(self, detectionMultiple):
        tmpList = [0]*10
        for i in range(len(detectionMultiple)):
            tmpList[len(detectionMultiple[i])] += 1
        return detectionMultiple[tmpList.index(max(tmpList))]

    def eliminerContoursProcheRobot(self):
        ileImpossible = []
        xRobot, yRobot = self.stationBase.getCarte().getRobot().getCentre()
        listIle = self.stationBase.getCarte().getIles()

        for i in range(len(listIle)):
            xIle, yIle = listIle[i].getCentre()
            if self.stationBase.getCarte().getTrajectoire().distanceADestinationAuCarre(xRobot, yRobot, xIle, yIle) <= 225:
                ileImpossible.append(i)

        if len(self.stationBase.carte.listeIles) == len(ileImpossible):
            self.stationBase.carte.listeIles = []
        elif not ileImpossible:
            self.stationBase.carte.listeIles = np.delete(self.stationBase.carte.listeIles, ileImpossible)

    def trouverRobot(self):
        detectionRobot = DetectionRobot(self.image, self.numeroTable)
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
        return self.stationBase.getCarte().getTrajectoire().distanceADestinationAuCarre(x, y, ancienX, ancienY) <= 225




