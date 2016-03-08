from PyQt4 import QtGui, QtCore
from elements.Carte import Carte
import ConfigPath


class ImageVirtuelle():
    def __init__(self, dimension):
        self.dimension_x, self.dimension_y = dimension
        self.carteVirtuelle = Carte
        self.listeIles = []
        self.listeTresors = []
        self.qp = QtGui.QPainter()

    def ajouterIles(self, listeIles):
        self.listeIles = listeIles

    def ajouterTresors(self, listeTresors):
        self.listeTresors = listeTresors

    def paintEvent(self, e):
        self.qp.begin(self)
        self.qp.drawPixmap(640, 350, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image_vide.png')), 0, 90, 640, 480)
        print("PAINT EVEN ###################")
        self.dessinerFormes()

    def dessinerFormes(self):
        for iles in self.listeIles:
            print("DESSINE")
            self.dessinerIles(iles)

    def dessinerIles(self, ile):
        position = (ile.centre_x, ile.centre_y)
        couleur = ile.couleur
        forme = ile.forme
        self.dessiner(forme, couleur, position)

    def definirCouleur(self, couleur):
        if (couleur == "Jaune"):
            self.qp.setBrush(QtGui.QColor(205, 175, 0, 250))
            self.qp.setPen(QtGui.QColor(205, 175, 0))
        elif (couleur == "Rouge"):
            self.qp.setBrush(QtGui.QColor(140, 0, 30, 250))
            self.qp.setPen(QtGui.QColor(140, 0, 30))
        elif (couleur == "Vert"):
            self.qp.setBrush(QtGui.QColor(0, 110, 60, 250))
            self.qp.setPen(QtGui.QColor(0, 110, 60))
        elif (couleur == "Bleu"):
            self.qp.setBrush(QtGui.QColor(0, 140, 190, 250))
            self.qp.setPen(QtGui.QColor(0, 140, 190))

    def dessiner(self, forme, couleur, position):
        self.definirCouleur(couleur)
        centre_x, centre_y = position

        if (forme == "Carre"):
            self.qp.drawRect(centre_x, centre_y, 30, 30)
        elif (forme == "Cercle"):
            self.qp.drawEllipse(centre_x, centre_y, 32, 32)
        elif (forme == "Triangle"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(centre_x - 18, centre_y + 12),
                QtCore.QPoint(centre_x, centre_y - 24),
                QtCore.QPoint(centre_x + 18, centre_y + 12)
            ])
            self.qp.drawConvexPolygon(polygone)

        elif (forme == "Pentagone"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(centre_x - 18, centre_y),
                QtCore.QPoint(centre_x, centre_y - 18),
                QtCore.QPoint(centre_x + 18, centre_y),
                QtCore.QPoint(centre_x + 9, centre_y + 18),
                QtCore.QPoint(centre_x - 9, centre_y + 18),
                QtCore.QPoint(centre_x - 18, centre_y)
            ])
            self.qp.drawConvexPolygon(polygone)
