import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionTresor import DetectionTresor
from threading import Thread
import time

class AnalyseImageEmbarquee(Thread):
    def __init__(self, robot, parametre):
        Thread.__init__(self)
        self.robot = robot
        self.parametre = parametre
        self.imageCamera = None
        self.alignementDepot = False
        self.ajustementsCalcules = False
        self.ajustements = []

    def run(self):
        while not (self.ajustementsCalcules):
            self._chargerImage()
            print("Thread analyseEmbarque run...")
            self.choisirAlignement(self.parametre)
            time.sleep(2)

        self.soumettreAjustements()
        print("Analyse terminee, ajustement soumis")

    def choisirAlignement(self, parametre):
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
        else:
            print("CRITICAL ERROR")

    def evaluerPositionTresor(self):
        self.detectionTresor = DetectionTresor(self.imageCamera)
        self.ajustements = self.detectionTresor.ajustements

        if (self.ajustements != []):
            print("Commandes ajustements PICKUP pretes")
            self.ajustementsCalcules = True
        else:
            print ("Ajustements non calculees (analyseimageembarque)")

    def evaluerPositionDepot(self, couleurIleCible):
        self.detectionIle = DetectionIle(self.imageCamera, couleurIleCible)
        self.ajustements = self.detectionIle.ajustements

        if (self.ajustements != []):
            print("Commandes ajustements DROP pretes")
            self.ajustementsCalcules = True

    def soumettreAjustements(self):
        for instructions in self.ajustements:
            print("Commandes envoyees a liste attente:" , instructions)
            self.robot.ajouterDirectives(instructions)

    def afficherFeed(self):
        cv2.imshow("Analyse", self.imageCamera)
        #cv2.waitKey(0)

    def _chargerImage(self):
        self.imageCamera = self.robot.threadVideo.getImageCapture()
        self._estomperImage()

    def _attendreFeedVideo(self):
        while self.robot.threadVideo.getImageCapture() is None:
            time.sleep(0.1)
            print("Problem here....")

    def _estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))