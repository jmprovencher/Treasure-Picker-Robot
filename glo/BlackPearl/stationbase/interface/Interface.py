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

import math


import sys
import ConfigPath
from stationbase.interface.StationBase import StationBase
from stationbase.interface.TensionCondensateur import TensionCondensateur
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
from stationbase.interface.AffichageDeBase import AffichageDeBase
import time

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.threadTensionCondensateur = TensionCondensateur()
        self.threadTensionCondensateur.start()
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
        self.direction = QLabel(self)
        self.direction.setGeometry(380, 52, 400, 80)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Demarer')
        self.btnDemarer.setGeometry(40, 70, 98, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.tensionCondensateur = QLabel(self)
        self.tensionCondensateur.setGeometry(480, 22, 640, 50)

    def demarerRoutine(self):
        self.threadStationBase = StationBase()
        self.threadStationBase.start()
        self.connect(self.threadAfficherImageVirtuelle, QtCore.SIGNAL("update()"), self.update_gui)
        self.threadAfficherImageVirtuelle.start()


    def update_gui(self):
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        QtGui.QApplication.processEvents()
        #if(not self.threadStationBase.carte.infoRobot is None):
            #self.orientation.setText(QString(str(self.threadStationBase.carte.infoRobot.centre_x) + 'x ' + str(self.threadStationBase.carte.infoRobot.centre_y) +'y '+ str(self.threadStationBase.carte.infoRobot.orientation)+'\xb0'))
        self.feed.repaint()
        self.tensionCondensateur.setText(QString(self.threadTensionCondensateur.tension))
        #self.orientation.repaint()
        #self.direction.repaint()
        self.tensionCondensateur.repaint()

    def dessinerDirection(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        vectorX = x2 - x1
        vectorY = y2 - y1
        #print(str(vectorX))
        self.direction.setText(QString(str(math.atan(vectorY/vectorX)*180/math.pi)))