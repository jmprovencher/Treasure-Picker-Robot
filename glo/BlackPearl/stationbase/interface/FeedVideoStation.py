import sys
from threading import Thread, RLock
import time
import cv2

verrou = RLock()

class FeedVideoStation(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.video = None
        self.initVideo(1)
        self.video.set(3,1600)
        self.video.set(4,1200)
        self.captureTable = None

    def run(self):
        while 1:
            with verrou:
                _, self.captureTable = self.video.read()
            cv2.imshow('Feed', self.captureTable)

    def initVideo(self, portCamera):
        self.video = cv2.VideoCapture(portCamera)
        while (not self.video.isOpened()):
            self.afficher('\na la recherche de la camera')
            self.video = cv2.VideoCapture(0)

    def afficher(self, string):
        sys.stdout.write(string)
        sys.stdout.flush()

    def getcaptureTable(self):
        with verrou:
            return self.captureTable

