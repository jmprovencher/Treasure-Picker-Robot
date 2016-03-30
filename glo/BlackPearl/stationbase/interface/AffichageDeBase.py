from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import QString

class AffichageDeBase():
    def __init__(self, qp):
        self.dessinerNoir(qp)
        qp.drawText(400, 80, QString('Orientation du robot : '))
        qp.drawText(400, 110, QString('Tension condensateur : '))
        qp.drawText(400, 50, QString('Position du robot : '))
        qp.drawText(400, 140, QString('Ile cible : '))
        self.formatContours(qp)
        self.dessinerNoir(qp)
        qp.drawText(275, 400 + 50, QString('88.95''N  15.10''O '))
        qp.drawText(275, 450 + 50, QString('1.23 V '))
        self.dessinerOrange(qp)
        self.dessinerNoir(qp)
        qp.drawText(880, 80, QString('Robot connecte?'))
        qp.drawEllipse(1000, 50, 50, 50)
        self.dessinerRouge(qp)
        qp.drawEllipse(1005, 55, 40, 40)

    def dessinerOrange(self, qp):
        qp.setBrush(QtGui.QColor(252, 100, 0, 250))
        qp.setPen(QtGui.QColor(252, 100, 0))

    def dessinerNoir(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 0, 250))
        qp.setPen(QtGui.QColor(0, 0, 0))

    def formatContours(self, qp):
        qp.setBrush(QtGui.QColor(250, 250, 250, 250))
        qp.setPen(QtGui.QColor(0, 0, 250))

    def dessinerRouge(self, qp):
        qp.setBrush(QtGui.QColor(240, 0, 0, 250))
        qp.setPen(QtGui.QColor(140, 0, 0))