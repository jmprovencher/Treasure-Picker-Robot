import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionStation import DetectionStation
from robot.vision.DetectionTresor import DetectionTresor
from robot.vision.DetectionOrientation import DetectionOrientation
from threading import Thread
import time
import numpy as np
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
        self.detectionTresor = DetectionTresor(self.imageCamera)
        self.detectionTresor.calculerAjustements()
        self.ajustements = self.detectionTresor.ajustements
        print("Nombre ajustement tresor: %d" %len(self.ajustements))
        if self.ajustements is None:
            self.robot.traiterCommande(('backward', 5))
            self._chargerImage()
            self.evaluerPositionTresor()

        if (self.ajustements != []):
            print("Ajustement calculer, analyse termine")
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
        intervalleJaune = np.array([0, 0, 0]), np.array([255, 255, 255]), "Jaune"
        intervalleFonce, intervalleClair, couleurForme = intervalleJaune
        masqueCouleur = cv2.inRange(self.imageCapture, intervalleFonce, intervalleClair)
        #kernel = np.ones((5, 5), np.uint8)
        #closing = cv2.morphologyEx(masqueCouleur, cv2.MORPH_CLOSE, kernel)
        #_, contoursCouleur, _ = cv2.findContours(masqueCouleur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("Tresor", masqueCouleur)
        cv2.waitKey(0)
        #self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('horizon.jpg'))
        self._estomperImage()

    def _attendreFeedVideo(self):
        while self.robot.threadVideo.getImageCapture() is None:
            time.sleep(0.5)
            print("Problem here....")

    def _estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))
