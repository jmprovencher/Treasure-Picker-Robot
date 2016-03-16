from PyQt4 import QtGui, QtCore
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import cv2

import ConfigPath
from stationbase.interface.FeedVideo import FeedVideo


class ImageReelle(object):
    def __init__(self, qp, image):
        self.qp = qp
        print("Image init")
        #cv2.imshow('image', image)
        self.imageCamera = image


    def updateImage(self):
        print("UPDATE IMAGE REELLE")
        #self.qp.drawPixmap(640, 0, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image7.png')), 0, 90, 640, 480)



