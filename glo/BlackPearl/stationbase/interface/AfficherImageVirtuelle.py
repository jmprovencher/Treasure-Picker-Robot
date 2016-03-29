from PyQt4 import QtGui, QtCore
import cv2
import numpy as np
import time
from PyQt4.QtCore import QThread
import ConfigPath

class AfficherImageVirtuelle(QThread):

    def __init__(self, interface):
        QThread.__init__(self)
        self.interface = interface
        self.imageConvertie = QtGui.QPixmap(ConfigPath.Config.appendToProjectPath('images/BlackPerl2.png'))

    def run(self):
        while self.interface.threadStationBase.threadImageVirtuelle is None or self.interface.threadStationBase.threadImageVirtuelle.imageVirtuelle is None:
            time.sleep(0.01)
        while 1:
            image = cv2.cvtColor(self.interface.threadStationBase.threadImageVirtuelle.imageVirtuelle, cv2.COLOR_BGR2RGB)
            self.convertirImage(image)
            self.emit(QtCore.SIGNAL("update()"))
            time.sleep(0.01)

    def convertirImage(self, image):
        image = QtGui.QImage(image, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).scaled(800, 600, QtCore.Qt.KeepAspectRatio)
        self.imageConvertie = QtGui.QPixmap.fromImage(image)