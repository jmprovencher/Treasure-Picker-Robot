import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionStation import DetectionStation
from robot.vision.DetectionTresor import DetectionTresor
from threading import Thread
import time

PARAMETRE_VERT = 0
PARAMETRE_BLEU = 1
PARAMETRE_JAUNE = 2
PARAMETRE_ROUGE = 3
PARAMETRE_TRESOR = 'tresor'
PARAMETRE_STATION = 'station'
PARAMETRE_ORIENTATION = 'orientation'


class AnalyseImageEmbarquee(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.imageCamera = None
        self.ajustementsCalcules = False
        self.ajustements = None
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
        if (self.ajustements is not None):
            self._soumettreAjustements()

    def debuterAlignement(self, parametre):
        if (parametre == PARAMETRE_VERT):
            self.evaluerPositionDepot('vert')
        elif (parametre == PARAMETRE_BLEU):
            self.evaluerPositionDepot('bleu')
        elif (parametre == PARAMETRE_JAUNE):
            self.evaluerPositionDepot('jaune')
        elif (parametre == PARAMETRE_ROUGE):
            self.evaluerPositionDepot('rouge')
        elif (parametre == PARAMETRE_TRESOR):
            self.evaluerPositionTresor()
        elif (parametre == PARAMETRE_STATION):
            self.evaluerPositionStation()
        elif (parametre == PARAMETRE_ORIENTATION):
            self.evaluerOrientation()
        else:
            print("CRITICAL ERROR")

    def evaluerPositionTresor(self):
        self.detectionTresor = DetectionTresor(self.imageCamera)
        self.detectionTresor.calculerAjustements()
        self.ajustements = self.detectionTresor.ajustements

        if (self.ajustements is not None):
            self.robot.tresorCapturer = True
        self.ajustementsCalcules = True


    def evaluerPositionStation(self):
        self.detectionStation = DetectionStation()
        self.detectionStation.trouverAjustements(self.imageCamera)
        self.ajustements = self.detectionStation.ajustements

        if (self.ajustements is not None):
            self.ajustementsCalcules = True

    def evaluerPositionDepot(self, couleurIleCible):
        self.detectionIle = DetectionIle()
        self.detectionIle.detecterIle(couleurIleCible, self.imageCamera)
        self.ajustements = self.detectionIle.ajustements

        if (self.ajustements is not None):
            self.ajustementsCalcules = True

    def _soumettreAjustements(self):
        for instructions in self.ajustements:
            self.robot.ajouterDirectives(instructions)


    def _chargerImage(self):
        self.imageCamera = self.robot.threadVideo.getImageCapture()
        self._estomperImage()

    def _attendreFeedVideo(self):
        while self.robot.threadVideo.getImageCapture() is None:
            time.sleep(0.5)
            print("En attente de la camera")

    def _estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))
