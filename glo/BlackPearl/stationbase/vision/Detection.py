import cv2


class Detection:
    def __init__(self, image, numeroTable):
        self.imageCamera = image
        self.numeroTable = numeroTable

    def trouverCentre(self, contourForme):
        MatriceCentreMasse = cv2.moments(contourForme)
        centre_x = int(round(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00']))
        centre_y = int(round(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00']))
        return centre_x, centre_y
