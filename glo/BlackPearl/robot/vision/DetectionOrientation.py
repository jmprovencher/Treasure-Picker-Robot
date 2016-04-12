import cv2
import math
from robot.alignement.AlignementMur import AlignementMur

class DetectionOrientation:
    def __init__(self, image):
        self.alignementMur= AlignementMur()
        self.imageCamera = image
        self.ajustements = []

    def calculerAjustementOrientation(self):
        orientation = self.trouverOrientation()
        if (abs(orientation) >= 2):
            ajustementOrientation = self.alignementMur.ajusterOrientation(orientation)
            print(ajustementOrientation)
            self.ajustements.append(ajustementOrientation)

    def trouverOrientation(self):
        imageGrise = cv2.cvtColor(self.imageCamera, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imageGrise, (3, 3), 0)
        filtreContours = cv2.Canny(blur, 225, 250)
        _, contours, hier = cv2.findContours(filtreContours.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow("Orientation", filtreContours)
        # cv2.waitKey(0)

        ligneHorizon = self.trouverLigneHorizon(contours)
        x0, y0, x1, y1 = self.trouverPointExtremeLigne(ligneHorizon)
        orientation = self.calculerOrientationHorizon(x0, y0, x1, y1)

        print("Orientation: %f" % orientation)
        # cv2.imshow("Orientation", self.imageCamera)
        # cv2.waitKey(0)
        return orientation

    def trouverLigneHorizon(self, contoursImage):
        maximum = cv2.arcLength(contoursImage[0], False)
        for cont in contoursImage:
            temp = cv2.arcLength(cont, False)
            if (temp > maximum):
                maximum = temp
                contour_max = cont
        return contour_max

    def trouverPointExtremeLigne(self, ligne):
        vx, vy, x, y = cv2.fitLine(ligne, cv2.DIST_L2, 0, 0.01, 0.01)
        pointGauche = int((-x * vy / vx) + y)
        pointDroit = int(((self.imageCamera.shape[1] - x) * vy / vx) + y)
        x0, y0 = (0, pointGauche)
        x1, y1 = (self.imageCamera.shape[1] - 1, pointDroit)
        cv2.line(self.imageCamera, (0, pointGauche), (self.imageCamera.shape[1] - 1, pointDroit), 255, 2)

        return x0, y0, x1, y1

    def calculerOrientationHorizon(self, x0, y0, x1, y1):
        mx, my = x1 - x0, y1 - y0
        roll = math.atan2(-mx, my)
        ajustement = math.degrees(roll) + 90
        return ajustement