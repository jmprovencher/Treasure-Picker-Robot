# import the necessary packages
import sys
from threading import Thread, RLock
import time
import cv2
from elements.Ile import Ile
from elements.Tresor import Tresor
from stationbase.vision.DetectionIles import DetectionIles
from stationbase.vision.DetectionRobot import DetectionRobot
from stationbase.vision.DetectionTresors import DetectionTresors

verrou = RLock()

class AnalyseImageWorld(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.police = cv2.FONT_HERSHEY_SIMPLEX
        self.image = None
        self.detectionPrimaire()

    def run(self):
        while 1:
            self.chargerImage()
            self.trouverRobot()
            time.sleep(1)

    def chargerImage(self):
        with verrou:
            self.image = self.stationBase.threadVideo.getcaptureTable()
        self.recadrerImage()
        self.estomperImage()

    def recadrerImage(self):
        self.image = self.image[155:1010, 0:1600]

    def estomperImage(self):
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

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


    def trouverRobot(self):
        print("\ndetection du robot")
        #self.detectionRobot = DetectionRobot(self.image)
        #self.detectionRobot.detecter()
        #self.detectionRobot.infoRobot
        #with verrou:
        #        self.stationBase.carte.infoRobot = infoRobot(centreForme, orientation)

'''
    def dessinerElementCartographique(self):
        for element in self.elementsCartographiques:
            cv2.putText(self.image, element.forme, (element.centre_x - 25, element.centre_y),
                        self.police, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


'''

