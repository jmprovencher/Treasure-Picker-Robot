import cv2
import numpy as np
import ConfigPath


class AlignementTresor(object):
    def __init__(self, image):
        self.imageCamera = image
        #cv2.imshow("image", image)
        #self.definirPositionOptimale()

    def definidefinirPositionOptimale(self):
        print("Uuiuuu")

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y