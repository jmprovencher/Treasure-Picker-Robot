import cv2
import ConfigPath
from robot.vision.DetectionIle import DetectionIle
from robot.vision.DetectionTresor import DetectionTresor

class AnalyseImageEmbarquee():
    def __init__(self):
        uiu = "showtime"

    def chargerImage(self, image):
        self.imageCamera = image
        self.estomperImage()
        #self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath(image))

    def estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))

    def evaluerPositionTresor(self):
        self.alignementTresor = DetectionTresor(self.imageCamera)

    def evaluerPositionDepot(self, couleurIleCible):
        self.alignementIle = DetectionIle(self.imageCamera, couleurIleCible)