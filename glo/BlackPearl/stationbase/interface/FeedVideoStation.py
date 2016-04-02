from threading import Thread
import cv2


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
        for camera_index in range(1, 10):
            try:
                self.video = cv2.VideoCapture(camera_index)
                self.video.set(3, 1600)
                self.video.set(4, 1200)
                success, self.captureTable = self.video.read()
                break
            except Exception as e:
                print e
                print('Mauvais index de camera...')





