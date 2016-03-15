# import the necessary packages
import sys

from robot.interface.Robot import Robot
from stationbase.interface.StationBase import StationBase
from stationbase.interface.ImageReelle import ImageReelle
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
from stationbase.interface.FeedVideo import FeedVideo
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter

import ConfigPath


class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')
        self.btnDemarrer = QtGui.QPushButton('Demarrer', self)
        self.btnVideo = QtGui.QPushButton('Start Video', self)
        self.btnDemarrer.resize(120, 46)
        self.btnVideo.resize(120, 46)
        self.btnDemarrer.move(200, 200)
        self.btnVideo.move(200, 300)
        self.ilesDetectees = []
        self.tresorsDetectes = []
        self.btnDemarrer.clicked.connect(self.demarrerRoutine)
        self.btnVideo.clicked.connect(self.demarrerCapture)
        self.demarre = False

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        if (self.estDemarrer()):
            image = self.obtenirImageReelle()
            imageReelle = ImageReelle(qp, image)
            imageVirtuelle = ImageVirtuelle(qp, self.ilesDetectees, self.tresorsDetectes)
        self.afficherInformations(qp)
        qp.end()

    def obtenirImageReelle(self):
        return self.stationBase.getImageReelle()

    def demarrerRoutine(self):
        self.feed = FeedVideo()
        self.stationBase = StationBase(self.feed)

    def demarrerCapture(self):
        self.stationBase.feedVideo.demarrerCapture()
        self.ilesDetectees = self.stationBase.carte.listeIles
        self.tresorsDetectes = self.stationBase.carte.listeTresors
        self.demarre = True
        self.repaint()

    def estDemarrer(self):
        return self.demarre

    def afficherInformations(self, qp):
        self.dessinerNoir(qp)
        qp.drawText(50, 400 + 50, QtCore.QString('Trajectoire :'))
        qp.drawText(50, 450 + 50, QtCore.QString('Tension condensateur :'))
        qp.drawText(50, 500 + 50, QtCore.QString('Position et Orientation du Robot :'))
        qp.drawText(50, 550 + 50, QtCore.QString('Ile cible :'))
        self.formatContours(qp)
        qp.drawRect(260, 385 + 50, 120, 20)
        qp.drawRect(260, 435 + 50, 80, 20)
        qp.drawRect(260, 485 + 50, 300, 20)
        qp.drawRect(260, 535 + 50, 100, 20)
        self.dessinerNoir(qp)
        qp.drawText(275, 400 + 50, QtCore.QString('88.95''N  15.10''O '))
        qp.drawText(275, 450 + 50, QtCore.QString('1.23 V '))
        qp.drawText(275, 500 + 50, QtCore.QString('0.8245m, 0.23421m     68.35''S  1.36''O '))
        qp.drawText(275, 550 + 50, QtCore.QString('Cercle rouge'))
        self.dessinerOrange(qp)
        qp.drawText(450, 338, QtCore.QString('Carte reelle'))
        qp.drawText(450, 378, QtCore.QString('Carte virtuelle'))
        qp.drawRect(450, 348, 830, 5)
        qp.drawRect(638, 0, 5, 700)

    def dessinerOrange(self, qp):
        qp.setBrush(QtGui.QColor(252, 100, 0, 250))
        qp.setPen(QtGui.QColor(252, 100, 0))

    def dessinerNoir(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 0, 250))
        qp.setPen(QtGui.QColor(0, 0, 0))

    def formatContours(self, qp):
        qp.setBrush(QtGui.QColor(250, 250, 250, 250))
        qp.setPen(QtGui.QColor(0, 0, 250))

def main():
    #robot = Robot()
    #robot.analyserImage()
    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
