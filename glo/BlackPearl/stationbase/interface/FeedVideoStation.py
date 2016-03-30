import sys
from threading import Thread, RLock
import time
import cv2

verrou = RLock()

class FeedVideoStation(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.video = None
        self.initVideo()
        self.captureTable = None
        self.feedEstDemare = False

    def run(self):
        while 1:
            success, self.captureTable = self.video.read()
            time.sleep(0.01)

    def initVideo(self):
        for camera_index in range(1, 10):
            try:
                self.video = cv2.VideoCapture(camera_index)
                #self.video = cv2.VideoCapture('test.webm')
                self.video.set(3,1600)
                self.video.set(4,1200)
                success, self.captureTable = self.video.read()
                self.feedEstDemare = True
                break
            except Exception as e:
                print('Mauvais index de camera...')





