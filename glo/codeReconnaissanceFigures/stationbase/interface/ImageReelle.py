import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import cv2
from PyQt4.QtGui import QPainter



import ConfigPath
from stationbase.interface.FeedVideo import FeedVideo


class ImageReelle():
    def __init__(self, image):
        print("Image init")
        cv2.imshow('image', image)
        self.imageCamera = image

    def updateImage(self, qp):
        print("UPDATE IMAGE REELLE")
        qp.drawPixmap(640, 0, QtGui.QPixmap(self.imageCamera), 0, 90, 640, 480)