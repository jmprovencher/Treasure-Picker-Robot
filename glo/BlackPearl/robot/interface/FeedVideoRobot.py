import cv2
from threading import Thread
import time
import numpy as np

class FeedVideoRobot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = None
        self.imageCapture = None
        self.capturer = False
        self.connecter = False

    def initialiserVideo(self):
        for camera_index in range(0, 10):
            try:
                self.video = cv2.VideoCapture(camera_index)
                self.video.set(3, 1600)
                self.video.set(4, 1200)
                _, self.imageCapture = self.video.read()
                self.connecter = True
                break
            except Exception as e:
                print('Mauvais index de camera...')

    def run(self):
        while (self.connecter):
            _, self.imageCapture = self.video.read()

    def getImageCapture(self):
        return self.imageCapture

    def demarrerCapture(self):
        if not (self.capturer):
            self.capturer = True

    def suspendreCapture(self):
        if (self.capturer):
            self.capturer = False
