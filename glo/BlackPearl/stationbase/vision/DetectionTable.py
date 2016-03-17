# import the necessary packages
import cv2
import numpy as np

class DetectionTable(object):
    def __init__(self, image):
        self.imageCamera = image
        self.tresorIdentifies = []
        self.intervalleVert = np.array([102, 255, 102]), np.array([0, 102, 0]), "Vert"

    def detecterCentreYCarreVert(self):
        intervalleClair, intervalleFonce, _ = self.intervalleVert
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contourPartielCarre = []
        contourCompletCarre = None
        for contour in contoursCouleur:
            x, y, w, h = cv2.boundingRect(contour)
            centre_x = x + (w / 2)
            centre_y = y + (h / 2)
            aire = w * h
            if ((centre_x > 600) and (centre_y > 200) and (centre_y < 1000) and (aire > 6000)):
                contourPartielCarre.append(contour)
                if (aire > 35000):
                    contourCompletCarre = contour
                    break

        yFinale = -1
        aireTotale = 0
        if (contourCompletCarre is None):
            for contour in contourPartielCarre:
                x, y, w, h = cv2.boundingRect(contour)
                aire = w * h
                centre_y = y + (h / 2)
                if (yFinale == -1):
                    yFinale = centre_y
                    aireTotale = aire
                else:
                    yFinale = (yFinale * aireTotale + centre_y * aire) / (aireTotale + aire) / 2
                    aireTotale = aireTotale + aire
        else:
            x, y, w, h = cv2.boundingRect(contourCompletCarre)
            yFinale = y + (h / 2)

        return int(yFinale)