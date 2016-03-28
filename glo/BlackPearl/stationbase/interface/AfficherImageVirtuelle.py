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
        self.imageNonConvertie = QtGui.QPixmap(ConfigPath.Config.appendToProjectPath('images/BlackPerl.png'))
        self.imageConvertie = self.imageNonConvertie.scaled(1200, 800, QtCore.Qt.KeepAspectRatio)


    def run(self):
        while self.interface.threadStationBase.threadImageVirtuelle is None or self.interface.threadStationBase.threadImageVirtuelle.imageVirtuelle is None:
            time.sleep(0.01)
        while 1:
            imageEnConvertion = cv2.cvtColor(self.interface.threadStationBase.threadImageVirtuelle.imageVirtuelle, cv2.COLOR_BGR2RGB)
            imageEnConvertion = QtGui.QImage(imageEnConvertion, imageEnConvertion.shape[1], imageEnConvertion.shape[0], QtGui.QImage.Format_RGB888)
            self.imageNonConvertie = QtGui.QPixmap.fromImage(imageEnConvertion)
            self.imageConvertie = self.imageNonConvertie.scaled(1200, 800, QtCore.Qt.KeepAspectRatio)
            self.emit(QtCore.SIGNAL("update()"))
            time.sleep(0.02)
