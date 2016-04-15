from threading import Thread
import cv2

RANGE_CAMERA_BAS = 1
RANGE_CAMERA_HAUT = 10

class FeedVideoStation(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = None
        self.captureTable = None
        self.initVideo()

    def run(self):
        while 1:
            success, self.captureTable = self.video.read()

    def initVideo(self):
        for camera_index in range(RANGE_CAMERA_BAS, RANGE_CAMERA_HAUT):
            try:
                self.video = cv2.VideoCapture(camera_index)
                self.video.set(3, 1600)
                success, self.captureTable = self.video.read()
                break
            except Exception as e:
                print e
                print('Mauvais index de camera...')





