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
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import QString


import sys
import ConfigPath
from stationbase.interface.StationBase import StationBase
from stationbase.interface.AffichageDeBase import AffichageDeBase
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
import time

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.initUI()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.affichageDeBase = AffichageDeBase(qp)
        qp.end()


    def initUI(self):
        self.setWindowTitle('Interface')
        self.resize(1600, 1000)
        self.setAutoFillBackground(False)
        self.feed = QLabel(self)
        self.feed.setGeometry(0, 145, 1600, 855)
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        self.orientation = QLabel(self)
        self.orientation.setGeometry(380, 22, 440, 50)
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
        if(not self.threadStationBase.carte.infoRobot is None):
            self.orientation.setText(QString(str(self.threadStationBase.carte.infoRobot.centre_x) + 'x ' + str(self.threadStationBase.carte.infoRobot.centre_y) +'y '+ str(self.threadStationBase.carte.infoRobot.orientation)+'\xb0'))
        self.feed.repaint()
        self.orientation.repaint()





