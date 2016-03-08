from PyQt4 import QtGui, QtCore
from elements.Carte import Carte


class ImageVirtuelle():
    def __init__(self, dimension):
        self.dimension_x, self.dimension_y = dimension
        self.carteVirtuelle = Carte
        self.listeIles = []
        self.listeTresors = []

    def ajouterIles(self, listeIles):
        self.listeIles = listeIles

    def ajouterTresors(self, listeTresors):
        self.listeTresors = listeTresors

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.dessiner(qp, "Triangle", "Jaune", 740, 592)
        qp.end()

    def dessinerIles(self):
        print("uiuiuiu")

    def dessiner(self, qp, forme, couleur, position_x, position_y):
        if (couleur == "Jaune"):
            qp.setBrush(QtGui.QColor(205, 175, 0, 250))
            qp.setPen(QtGui.QColor(205, 175, 0))
        elif (couleur == "Rouge"):
            qp.setBrush(QtGui.QColor(140, 0, 30, 250))
            qp.setPen(QtGui.QColor(140, 0, 30))
        elif (couleur == "Vert"):
            qp.setBrush(QtGui.QColor(0, 110, 60, 250))
            qp.setPen(QtGui.QColor(0, 110, 60))
        elif (couleur == "Bleu"):
            qp.setBrush(QtGui.QColor(0, 140, 190, 250))
            qp.setPen(QtGui.QColor(0, 140, 190))

        if (forme == "Carre"):
            qp.drawRect(position_x, position_y, 30, 30)
        elif (forme == "Cercle"):
            qp.drawEllipse(position_x, position_y, 32, 32)
        elif (forme == "Triangle"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(position_x - 18, position_y + 12),
                QtCore.QPoint(position_x, position_y - 24),
                QtCore.QPoint(position_x + 18, position_y + 12)
            ])
            qp.drawConvexPolygon(polygone)
        elif (forme == "Pentagone"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(position_x - 18, position_y),
                QtCore.QPoint(position_x, position_y - 18),
                QtCore.QPoint(position_x + 18, position_y),
                QtCore.QPoint(position_x + 9, position_y + 18),
                QtCore.QPoint(position_x - 9, position_y + 18),
                QtCore.QPoint(position_x - 18, position_y)
            ])
            qp.drawConvexPolygon(polygone)
