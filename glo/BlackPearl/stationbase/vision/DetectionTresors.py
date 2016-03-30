# import the necessary packages
import cv2
import numpy as np
import ConfigPath


class DetectionTresors(object):
    def __init__(self, image):
        self.imageCamera = image
        self.tresorIdentifies = []

    def detecter(self):
        #table 2
        #intervalleFoncer = np.array([50, 160, 160])
        #intervalleClair = np.array([6, 100, 100])

        #table 1
        intervalleFoncer = np.array([30, 160, 150])
        intervalleClair = np.array([0, 53, 50])

        #intervalleFoncer = np.array([41, 70, 84])
        #intervalleClair = np.array([0 , 53 ,50])

        shapeTresorMasque = cv2.inRange(self.imageCamera, intervalleClair, intervalleFoncer)
        cv2.imshow('tresore',shapeTresorMasque)
        #cv2.waitKey(0)
        _, contoursTresor, _ = cv2.findContours(shapeTresorMasque.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contoursNegligeable = []
        for contours in range(len(contoursTresor)):
            aire = cv2.contourArea(contoursTresor[contours])
            if (aire < 30 or aire > 150):
                contoursNegligeable.append(contours)

        if len(contoursTresor) == len(contoursNegligeable):
            contoursTresor = []
        elif (contoursNegligeable != []):
            contoursTresor = np.delete(contoursTresor, contoursNegligeable)

        if len(contoursTresor) > 0:
            for contours in contoursTresor:
                formeTresor = contours, "Tresor", ""
                #print "Ajout tresor"
                self.tresorIdentifies.append(formeTresor)

