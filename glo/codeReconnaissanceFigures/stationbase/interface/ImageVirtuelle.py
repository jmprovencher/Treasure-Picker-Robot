from PyQt4 import QtGui, QtCore

class ImageVirtuelle():
    def __init__(self, dimension):
        self.dimension_x, self.dimension_y = dimension
        self.dessinerCarre(qp)
        self.dessinerCercle(qp)
        self.dessinerPentagone(qp)
        self.dessinerTriangle(qp)

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