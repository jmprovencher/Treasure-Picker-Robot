import cv2
import numpy as np
import ConfigPath


class DetectionTresor(object):
    def __init__(self, image):
        self.imageCamera = image
        self.positionZone = (810, 730)
        self.rayonZone = 20
        #cv2.imshow("image", image)
        #self.definirPositionOptimale()

    def dessinerZoneCritique(self):
        cv2.circle(self.imageCamera, self.positionZone, self.rayonZone, (0, 255, 0), 2)

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y