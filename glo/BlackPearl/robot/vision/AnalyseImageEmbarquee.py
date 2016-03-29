import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionTresor import DetectionTresor
from threading import Thread
import time

COULEUR_CIBLE = "Bleu"


class AnalyseImageEmbarquee(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.imageCamera = None
        self.detectionTresor = False
        self.alignementDepot = False
        self.ajustementsCalcules = False
        self.ajustements = []

    def attendreFeedVideo(self):
        while self.robot.threadVideo.getImageCapture() is None:
            time.sleep(0.01)

    def run(self):
        self.chargerImage()
        while not (self.ajustementsCalcules):
            print("Thread analyseEmbarque run...")
            if (self.alignementDepot):
                self.evaluerPositionDepot(COULEUR_CIBLE)
            else:
                self.evaluerPositionTresor()
                self.afficherFeed()
            time.sleep(1)
        print("Pret a soumettre ajustement")
        self.soumettreAjustements()

    def chargerImage(self):
        #peut etre pas necessaire
        #self.attendreFeedVideo()
        #self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('images/camera_robot/tresors/test_image5.png'))
        self.imageCamera = self.robot.threadVideo.getImageCapture()
        self._estomperImage()

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
            self.robot.ajouterCommande(instructions)

    def afficherFeed(self):
        cv2.imshow("Analyse", self.imageCamera)
        #cv2.waitKey(0)

    def _estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))