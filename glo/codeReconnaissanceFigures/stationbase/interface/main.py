# import the necessary packages
import sys
from stationbase.interface.StationBase import StationBase
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot


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
        self.dessinerCarre(qp)
        self.dessinerCercle(qp)
        self.dessinerPentagone(qp)
        self.dessinerTriangle(qp)
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
        qp.drawPixmap(640, 0, QtGui.QPixmap('images/test_image7.png'), 0, 90, 640, 480)
        qp.drawPixmap(640, 350, QtGui.QPixmap('images/test_image_vide.png'), 0, 90, 640, 480)
        self.dessinerOrange(qp)
        qp.drawRect(450, 348, 830, 5)
        qp.drawRect(638, 0, 5, 700)
        qp.drawText(450, 338, QtCore.QString('Carte reelle'))
        qp.drawText(450, 378, QtCore.QString('Carte virtuelle'))

    def dessinerCarre(self, qp):
        self.dessinerVert(qp)
        qp.drawRect(953, 457, 30, 30)

        self.dessinerBleu(qp)
        qp.drawRect(823, 578, 30, 30)

    def dessinerCercle(self, qp):
        self.dessinerRouge(qp)
        qp.drawEllipse(807, 442, 32, 32)

    def dessinerPentagone(self, qp):
        self.dessinerJaune(qp)
        self.initPentagone(qp, 900, 592)

    def dessinerTriangle(self, qp):
        self.dessinerJaune(qp)
        self.initTriangle(qp, 722, 568)

    def initTriangle(self, qp, x, y):
        polygone = QtGui.QPolygon([
            QtCore.QPoint(x + 0, y + 36),
            QtCore.QPoint(x + 18, y + 0),
            QtCore.QPoint(x + 36, y + 36)
        ])
        qp.drawConvexPolygon(polygone)

    def initPentagone(self, qp, x, y):
        polygone = QtGui.QPolygon([
            QtCore.QPoint(x + 0, y + 18),
            QtCore.QPoint(x + 18, y),
            QtCore.QPoint(x + 36, y + 18),
            QtCore.QPoint(x + 27, y + 36),
            QtCore.QPoint(x + 9, y + 36),
            QtCore.QPoint(x + 0, y + 18)
        ])
        qp.drawConvexPolygon(polygone)

    def formatContours(self, qp):
        qp.setBrush(QtGui.QColor(250, 250, 250, 250))
        qp.setPen(QtGui.QColor(0, 0, 250))

    def dessinerNoir(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 0, 250))
        qp.setPen(QtGui.QColor(0, 0, 0))

    def dessinerOrange(self, qp):
        qp.setBrush(QtGui.QColor(252, 100, 0, 250))
        qp.setPen(QtGui.QColor(252, 100, 0))

    def dessinerJaune(self, qp):
        qp.setBrush(QtGui.QColor(205, 175, 0, 250))
        qp.setPen(QtGui.QColor(205, 175, 0))

    def dessinerRouge(self, qp):
        qp.setBrush(QtGui.QColor(140, 0, 30, 250))
        qp.setPen(QtGui.QColor(140, 0, 30))

    def dessinerVert(self, qp):
        qp.setBrush(QtGui.QColor(0, 110, 60, 250))
        qp.setPen(QtGui.QColor(0, 110, 60))

    def dessinerBleu(self, qp):
        qp.setBrush(QtGui.QColor(0, 140, 190, 250))
        qp.setPen(QtGui.QColor(0, 140, 190))


def main():
    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
