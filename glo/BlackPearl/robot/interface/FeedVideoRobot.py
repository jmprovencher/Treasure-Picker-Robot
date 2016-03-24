import cv2
from threading import Thread
import time

CAMERA_INDEX = 0


class FeedVideoRobot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = None
        self.initialiserVideo(CAMERA_INDEX)
        self.video.set(3,1600)
        self.video.set(4,1200)
        self.imageCapture = None

    def initialiserVideo(self, portCamera):
        self.video = cv2.VideoCapture(portCamera)
        while not (self.video.isOpened()):
            print("Camera introuvable, essaye un autre index...")
            self.video = cv2.VideoCapture(1)

    def run(self):
        while 1:
            print ("RobotFeed thread is running...")
            _, self.imageCapture = self.video.read()
            cv2.imshow("LIVE FEED", self.imageCapture)
            time.sleep(0.2)


    def getImageCapture(self):
        return self.imageCapture