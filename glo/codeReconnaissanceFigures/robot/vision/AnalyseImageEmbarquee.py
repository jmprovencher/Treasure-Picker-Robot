import cv2
import ConfigPath
from robot.vision.AlignementIle import AlignementIle
from robot.vision.AlignementTresor import AlignementTresor

class AnalyseImageEmbarquee():
    def __init__(self):
        uiu = "showtime"

    def chargerImage(self, image):
        #self.imageCamera = image
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath(image))

    def estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))

    def evaluerPositionTresor(self):
        self.alignementTresor = AlignementTresor(self.imageCamera)

    def evaluerPositionDepot(self, couleurIleCible):
        self.alignementIle = AlignementIle(self.imageCamera, couleurIleCible)