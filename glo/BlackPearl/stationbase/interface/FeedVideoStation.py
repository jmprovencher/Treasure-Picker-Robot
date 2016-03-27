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
        self.captureTable = None
        self.feedEstDemare = False

    def run(self):
        while 1:
            success, self.captureTable = self.video.read()
            #if (success):
                #cv2.imshow('Feed', self.captureTable)
            time.sleep(0.01)

    def initVideo(self, portCamera):
        self.video = cv2.VideoCapture(portCamera)
        self.video.set(3,1600)
        self.video.set(4,1200)
        while (not self.video.isOpened()):
            print('\na la recherche de la camera')
            self.video = cv2.VideoCapture(portCamera)
        success, self.captureTable = self.video.read()
        self.feedEstDemare = True




