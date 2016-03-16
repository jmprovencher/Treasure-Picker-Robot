import cv2


class FeedVideo(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.enregistre = False
        self._observers = []
        self._imageCapture = 0
        self.img = 0

    def demarrerCapture(self):
        self._capturer()
        self.enregistre = True

    def get_image(self):
        return self._imageCapture

    def set_image(self, image):
        self._imageCapture = image
        for callback in self._observers:
            callback(self._imageCapture)

    imageCapture = property(get_image, set_image)

    def bind_to(self, callback):
        self._observers.append(callback)

    def _capturer(self):
        # On enregistre toutes les x millisecondes
        while cv2.waitKey(1000) == -1:
            print ("Capturing ")
            ret, frame = self.capture.read()
            self.img = frame
            self.set_image(frame)
            cv2.imshow('image', self._imageCapture)
        if (self.enregistre == False):
            blur = cv2.blur(self._imageCapture, (5, 5))

    def suspendreCapture(self):
        self.enregistre = False

    def reprendreCapture(self):
        self.enregistre = True

