import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionTresor import DetectionTresor
from threading import Thread

COULEUR_CIBLE = "Bleu"

class AnalyseImageEmbarquee(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.imageCamera = None
        self.alignementTresor = False
        self.alignementDepot = False

    def run(self):
        print("Analyse run...")
        self.chargerImage()
        if (self.robot.alignementDepot):
            self.evaluerPositionDepot(COULEUR_CIBLE)
        else:
            self.evaluerPositionTresor()

    def chargerImage(self):
        self.imageCamera = self.robot.threadVideo.getImageCapture()
        self.estomperImage()

    def estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))

    def evaluerPositionTresor(self):
        self.alignementTresor = DetectionTresor(self.imageCamera)

    def evaluerPositionDepot(self, couleurIleCible):
        self.alignementIle = DetectionIle(self.imageCamera, couleurIleCible)