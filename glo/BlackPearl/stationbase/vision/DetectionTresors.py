import cv2
import numpy as np

class DetectionTresors(object):
    def __init__(self, image, numeroTable):
        self.imageCamera = image
        self.numeroTable = numeroTable
        self.tresorIdentifies = []

    def detecter(self):
        contoursTresor = self.trouverContoursTresors()
        contoursTresor = self.eleminerCoutoursNegligeable(contoursTresor)
        self.trouverTresors(contoursTresor)

    def trouverContoursTresors(self):
        if (self.numeroTable == 2 or self.numeroTable == 3):
            intervalleFoncer, intervalleClair = (np.array([50, 160, 160]), np.array([6, 100, 100]))
        elif (self.numeroTable == 1):
            intervalleFoncer, intervalleClair = (np.array([30, 160, 150]), np.array([0, 53, 50]))
        elif (self.numeroTable == 5 or self.numeroTable == 6):
            intervalleFoncer, intervalleClair = (np.array([41, 70, 84]), np.array([0 , 53 ,50]))

        shapeTresorMasque = cv2.inRange(self.imageCamera, intervalleClair, intervalleFoncer)
        _, contoursTresor, _ = cv2.findContours(shapeTresorMasque.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contoursTresor

    def eleminerCoutoursNegligeable(self, contoursTresor):
        contoursNegligeables = []

        for i in range(len(contoursTresor)):
            aire = cv2.contourArea(contoursTresor[i])
            if (aire < 30 or aire > 150):
                contoursNegligeables.append(i)

        if len(contoursTresor) == len(contoursNegligeables):
            contoursTresor = []
        elif (contoursNegligeables != []):
            contoursTresor = np.delete(contoursTresor, contoursNegligeables)

        return contoursTresor

    def trouverTresors(self, contoursTresor):
        if len(contoursTresor) > 0:
            for contours in contoursTresor:
                formeTresor = contours, "Tresor", ""
                self.tresorIdentifies.append(formeTresor)
