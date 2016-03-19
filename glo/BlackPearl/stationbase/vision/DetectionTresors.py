# import the necessary packages
import cv2
import numpy as np
import ConfigPath


class DetectionTresors(object):
    def __init__(self, image):
        self.imageCamera = image
        self.tresorIdentifies = []

    def detecter(self):

        intervalleClair = np.array([37, 145, 145])
        intervalleFoncer = np.array([6, 100, 100])

        shapeTresorMasque = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)
        _, contoursTresor, _ = cv2.findContours(shapeTresorMasque.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contoursNegligeable = []
        for contours in range(len(contoursTresor)):
            aire = cv2.contourArea(contoursTresor[contours])
            if (aire < 30 or aire > 150):
                contoursNegligeable.append(contours)

        if (contoursNegligeable != []):
            contoursTresor = np.delete(contoursTresor, contoursNegligeable)

        for contours in contoursTresor:
            formeTresor = contours, "Tresor", ""
            print "Ajout tresor"
            self.tresorIdentifies.append(formeTresor)

        