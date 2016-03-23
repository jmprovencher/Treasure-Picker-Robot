# import the necessary packages
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import QMetaObject
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QButtonGroup
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
import sys
import ConfigPath
from stationbase.interface.StationBase import StationBase
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
import time

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interface')
        self.resize(1600, 1000)
        self.setAutoFillBackground(False)

        self.feed = QLabel(self)
        self.feed.setGeometry(0, 145, 1600, 855)
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)

        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Demarer')
        self.btnDemarer.setGeometry(40, 70, 98, 27)

        self.btnDemarer.clicked.connect(self.demarerRoutine)

    def demarerRoutine(self):
        self.threadStationBase = StationBase()
        self.threadStationBase.start()
        self.connect(self.threadAfficherImageVirtuelle, QtCore.SIGNAL("update()"), self.update_gui)
        self.threadAfficherImageVirtuelle.start()

    def update_gui(self):
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        QtGui.QApplication.processEvents()
        self.feed.repaint()




