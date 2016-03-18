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
        self.elementsCartographiques = []
        self.tresorIdentifies = []
        self.ilesIdentifiees = []
        self.infoRobot = None
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
        print("\ndetection des iles et tresors")
        self.detectionIles = DetectionIles(self.image)
        self.detectionTresors = DetectionTresors(self.image)
        self.detectionIles.detecter()
        self.detectionTresors.detecter()
        self.ilesIdentifiees = self.detectionIles.ilesIdentifiees
        self.tresorIdentifies = self.detectionTresors.tresorIdentifies
        for element in self.ilesIdentifiees:
            self.identifierForme(element)
        for tresor in self.tresorIdentifies:
            self.identifierForme(tresor)
        self.trouverRobot()


    def trouverRobot(self):
        print("\ndetection du robot")
        self.detectionRobot = DetectionRobot(self.image)
        #self.detectionRobot.detecter()
        #self.infoRobot = self.detectionRobot.getInfoRobot()

'''
    def dessinerTrajet(self, trajet):
        pointInitial = None

        if (len(trajet) == 0):
            cv2.putText(self.image, 'Aucun trajet disponible', (1000, 800), self.police, 1.5,
                        (0, 0, 255), 2, cv2.LINE_AA)
        else:
            for pointFinal in trajet:
                if (pointInitial == None):
                    pointInitial = pointFinal
                else:
                    cv2.arrowedLine(self.image, pointFinal, pointInitial, (0, 255, 0), 5)
                    pointInitial = pointFinal

    def dessinerElementCartographique(self):
        for element in self.elementsCartographiques:
            cv2.putText(self.image, element.forme, (element.centre_x - 25, element.centre_y),
                        self.police, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def dessinerDebutFinTrajet(self, pointInitial, pointFinal):
        debut_x, debut_y = pointInitial
        fin_x, fin_y = pointFinal

        cv2.putText(self.image, 'Debut', (debut_x - 25, debut_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.image, 'Fin', (fin_x, fin_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)
'''

