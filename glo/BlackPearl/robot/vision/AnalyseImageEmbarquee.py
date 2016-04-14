import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionStation import DetectionStation
from robot.vision.DetectionTresor import DetectionTresor
from robot.vision.DetectionOrientation import DetectionOrientation
from threading import Thread
import time


class AnalyseImageEmbarquee(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.imageCamera = None
        self.ajustementsCalcules = False
        self.ajustements = []
        self.parametre = None
        self.nombreDetection = 0

    def definirType(self, parametre):
        self.parametre = parametre

    def run(self):
        while not (self.ajustementsCalcules) and (self.parametre is not None):
            time.sleep(1)
            self._chargerImage()
            self.debuterAlignement(self.parametre)
            time.sleep(1)
        self._soumettreAjustements()

    def debuterAlignement(self, parametre):
        if (parametre == 0):
            self.evaluerPositionDepot('vert')
        elif (parametre == 1):
            self.evaluerPositionDepot('bleu')
        elif (parametre == 2):
            self.evaluerPositionDepot('jaune')
        elif (parametre == 3):
            self.evaluerPositionDepot('rouge')
        elif (parametre == 'tresor'):
            self.evaluerPositionTresor()
        elif (parametre == 'station'):
            self.evaluerPositionStation()
        elif (parametre == 'station_final'):
            self.evaluerPositionStationFinal()
        elif (parametre == 'orientation'):
            self.evaluerOrientation()
        else:
            print("CRITICAL ERROR")

    def evaluerOrientation(self):
        self.detectionOrientation = DetectionOrientation(self.imageCamera)
        self.detectionOrientation.calculerAjustementOrientation()
        self.ajustements = self.detectionOrientation.ajustements

        if (self.ajustements != []):
            print("Ajustement calculer, analyse termine")
            self.ajustementsCalcules = True

    def evaluerPositionTresor(self):
        self.detectionTresor = DetectionTresor()
        self.detectionTresor.calculerAjustements(self.imageCamera)
        self.ajustements = self.detectionTresor.ajustements

        while self.ajustements is None and self.nombreDetection < 5:
            self.robot.traiterCommande('backward', 1)
            time.sleep(1)
            self._chargerImage()
            self.detectionTresor.calculerAjustements(self.imageCamera)
            self.ajustements = self.detectionTresor.ajustements
            self.nombreDetection + 1
            print("Nombre detection", self.nombreDetection)

        if (self.ajustements is None) and self.nombreDetection == 5:
            self.robot.tresorNonCapturer = True

        if (self.ajustements is not None):
            print("Nombre ajustement tresor: %d" % len(self.ajustements))
            self.ajustementsCalcules = True
            self.robot.tresorCapturer = True

    def evaluerPositionStation(self):
        self.detectionStation = DetectionStation()
        self.detectionStation.trouverAjustements(self.imageCamera)
        self.ajustements = self.detectionStation.ajustements

        while self.ajustements is None and self.nombreDetection < 5:
            self.robot.traiterCommande('right', 1)
            self._chargerImage()
            self.evaluerPositionStation()
            self.nombreDetection + 1

        if (self.ajustements is not None):
            self.ajustementsCalcules = True

    def evaluerPositionStationFinal(self):
        self.detectionStation = DetectionStation(self.imageCamera)
        self.detectionStation.trouverAjustementsFinaux()
        self.ajustements = self.detectionStation.ajustements

        while self.ajustements is None and self.nombreDetection < 5:
            self.robot.traiterCommande('backward', 1)
            self._chargerImage()
            self.evaluerPositionStation()
            self.nombreDetection + 1

        if (self.ajustements is not None):
            self.ajustementsCalcules = True

    def evaluerPositionDepot(self, couleurIleCible):
        self.detectionIle = DetectionIle(self.imageCamera)
        self.detectionIle.detecterIle(couleurIleCible)
        self.ajustements = self.detectionIle.ajustements

        while self.ajustements is None and self.nombreDetection < 3:
            self.robot.traiterCommande('forward', 1)
            self._chargerImage()
            self.evaluerPositionDepot()
            self.nombreDetection + 1

        if (self.ajustements is not None):
            self.ajustementsCalcules = True

    def _soumettreAjustements(self):
        for instructions in self.ajustements:
            self.robot.ajouterDirectives(instructions)

    def _afficherFeed(self):
        cv2.imshow("Analyse", self.imageCamera)
        cv2.waitKey(0)

    def _chargerImage(self):
        self.imageCamera = self.robot.threadVideo.getImageCapture()
        #self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('image1.png'))
        self._estomperImage()

    def _attendreFeedVideo(self):
        while self.robot.threadVideo.getImageCapture() is None:
            time.sleep(0.5)
            print("Problem here....")

    def _estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))
