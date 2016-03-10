from PyQt4 import QtGui, QtCore
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import ConfigPath
class ImageReelle():
    def __init__(self, qp):
        self.qp = qp
        qp.drawPixmap(640, 0, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image7.png')), 0, 90, 640, 480)

