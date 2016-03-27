from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import QString

class AffichageDeBase():
    def __init__(self, qp):
        self.dessinerNoir(qp)
        qp.drawText(200, 80, QString('Orientation du robot : '))
        qp.drawText(200, 110, QString('Tension condensateur : '))
        qp.drawText(200, 50, QString('Position du robot : '))
        qp.drawText(50, 550 + 50, QString('Ile cible :'))
        self.formatContours(qp)
        self.dessinerNoir(qp)
        qp.drawText(275, 400 + 50, QString('88.95''N  15.10''O '))
        qp.drawText(275, 450 + 50, QString('1.23 V '))
        self.dessinerOrange(qp)
        #qp.drawText(805, 133, QString('Carte virtuelle'))
        #qp.drawRect(0, 140, 1599, 5)
        #qp.drawRect(780, 110, 120, 5)
        #qp.drawRect(780, 110, 5, 30)
        #qp.drawRect(900, 110, 5, 30)
        self.dessinerNoir(qp)
        qp.drawText(1280-200, 80, QString('Robot connecte?'))
        qp.drawEllipse(1400-200, 50, 50, 50)
        self.dessinerRouge(qp)
        qp.drawEllipse(1405-200, 55, 40, 40)

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