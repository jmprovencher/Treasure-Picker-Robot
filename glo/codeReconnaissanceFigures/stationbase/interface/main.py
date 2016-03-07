# import the necessary packages
import sys
from stationbase.interface.StationBase import StationBase
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

import ConfigPath


class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')
        btnDemarrer = QtGui.QPushButton('Demarrer', self)
        btnDemarrer.clicked.connect(self.demarrerRoutine)
        btnDemarrer.resize(120, 46)
        btnDemarrer.move(200, 200)

    @pyqtSlot()
    def demarrerRoutine(self):
        self.initialiserStationBase()

    def initialiserStationBase(self):
        self.stationBase = StationBase()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)

        self.afficherInformations(qp)
        self.afficherImages(qp)
        qp.end()

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

    def afficherImages(self, qp):
        qp.drawPixmap(640, 0, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image7.png')), 0, 90, 640, 480)
        qp.drawPixmap(640, 350, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image_vide.png')), 0, 90, 640, 480)
        self.dessinerOrange(qp)
        qp.drawRect(450, 348, 830, 5)
        qp.drawRect(638, 0, 5, 700)
        qp.drawText(450, 338, QtCore.QString('Carte reelle'))
        qp.drawText(450, 378, QtCore.QString('Carte virtuelle'))

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
    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
