import cv2
from threading import Thread
import time


class FeedVideoRobot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = None
        self.initialiserVideo()
        self.video.set(3, 1600)
        self.video.set(4, 1200)
        self.imageCapture = None
        self.capturer = False
        self.connecter = False

    def initialiserVideo(self):
        for camera_index in range(1, 4):
            try:
                self.video = cv2.VideoCapture(camera_index)
                _, self.imageCapture = self.video.read()
                self.connecter = True
                break
            except Exception as e:
                print('Mauvais index de camera...')

    def run(self):
        while 1:
            print ("Streaming only...")
            _, self.imageCapture = self.video.read()
            time.sleep(0.5)
            # cv2.imshow("LIVE FEED", self.imageCapture)

    def getImageCapture(self):
        ("Streamed image was accessed...")
        return self.imageCapture

    def libererCamera(self):
        self.video.release()
