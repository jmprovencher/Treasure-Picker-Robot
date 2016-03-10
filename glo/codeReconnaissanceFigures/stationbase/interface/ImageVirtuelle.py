from PyQt4 import QtGui, QtCore

import ConfigPath


class ImageVirtuelle():
    def __init__(self, qp, listeIles, listeTresors):
        qp.drawPixmap(640, 350, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image_vide.png')), 0, 90, 640, 480)
        print("PAINT EVEN ###################")
        self.dessinerIles(qp, listeIles)
        self.dessinerTresors(qp, listeTresors)

    def dessinerTresors(self, qp, listeTresors):
        for tresor in listeTresors:
            position = tresor.centre_x * 0.4 + 618, tresor.centre_y * 0.4 + 355
            self.dessinerTresor(qp, position)

    def dessinerIles(self, qp, listeIles):
        for ile in listeIles:
            print("DESSINE")
            position = (ile.centre_x * 0.4 + 618, ile.centre_y * 0.4 + 355)
            couleur = ile.couleur
            forme = ile.forme
            self.dessiner(qp, forme, couleur, position)


    def definirCouleur(self, qp, couleur):
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

    def dessinerTresor(self, qp, position):
        centre_x, centre_y = position
        qp.setBrush(QtGui.QColor(205, 175, 0, 250))
        qp.setPen(QtGui.QColor(205, 175, 0))
        qp.drawRect(centre_x, centre_y, 10, 4)


    def dessiner(self, qp, forme, couleur, position):
        centre_x, centre_y = position
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
            qp.drawRect(centre_x - 15, centre_y -15, 30, 30)
        elif (forme == "Cercle"):
            qp.drawEllipse(centre_x - 16, centre_y - 16, 32, 32)
        elif (forme == "Triangle"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(centre_x - 18, centre_y + 12),
                QtCore.QPoint(centre_x, centre_y - 24),
                QtCore.QPoint(centre_x + 18, centre_y + 12)
            ])
            qp.drawConvexPolygon(polygone)

        elif (forme == "Pentagone"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(centre_x - 18, centre_y),
                QtCore.QPoint(centre_x, centre_y - 18),
                QtCore.QPoint(centre_x + 18, centre_y),
                QtCore.QPoint(centre_x + 9, centre_y + 18),
                QtCore.QPoint(centre_x - 9, centre_y + 18),
                QtCore.QPoint(centre_x - 18, centre_y)
            ])
            qp.drawConvexPolygon(polygone)