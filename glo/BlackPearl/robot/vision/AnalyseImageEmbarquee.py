import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionStation import DetectionStation
from robot.vision.DetectionTresor import DetectionTresor
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
        if (parametre == 'bleu'):
            self.evaluerPositionDepot('bleu')
        elif (parametre == 'vert'):
            self.evaluerPositionDepot('vert')
        elif (parametre == 'rouge'):
            self.evaluerPositionDepot('rouge')
        elif (parametre == 'jaune'):
            self.evaluerPositionDepot('jaune')
        elif (parametre == 'tresor'):
            self.evaluerPositionTresor()
        elif (parametre == 'station'):
            self.evaluerPositionStation()
        else:
            print("CRITICAL ERROR")

    def evaluerPositionTresor(self):
        self.detectionTresor = DetectionTresor(self.imageCamera)
        self.ajustements = self.detectionTresor.ajustements
        if (self.ajustements != []):
            self.ajustementsCalcules = True

    def evaluerPositionStation(self):
        self.detectionStation = DetectionStation(self.imageCamera)
        self.detectionStation.trouverAjustements()
        self.ajustements = self.detectionStation.ajustements

        if (self.ajustements != []):
            self.ajustementsCalcules = True

    def evaluerPositionDepot(self, couleurIleCible):
        self.detectionIle = DetectionIle(self.imageCamera)
        self.detectionIle.detecterIle(couleurIleCible)
        self.ajustements = self.detectionIle.ajustements

        if (self.ajustements != []):
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
