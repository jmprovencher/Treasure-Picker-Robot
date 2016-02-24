import sys
from PyQt4 import QtGui, QtCore

class Interface(QtGui.QWidget):

    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')
        btn = QtGui.QPushButton('DEMARAGE', self)
        btn.resize(120,46)
        btn.move(200, 200)


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)


        self.setUpLiveFeed(qp)
        self.setUpLiveVirtuel(qp)
        self.drawRectangles(qp)
        self.drawCircles(qp)
        self.drawPolygones(qp)
        self.drawTriangles(qp)
        qp.end()

    def setUpLiveFeed(self, qp):
        self.noir(qp)
        qp.drawText(50, 400 + 50, QtCore.QString("Trajectoire :"))
        qp.drawText(50, 450 + 50, QtCore.QString("Tension condensateur :"))
        qp.drawText(50, 500 + 50, QtCore.QString("Position et Orientation du Robot :"))
        qp.drawText(50, 550 + 50, QtCore.QString("Ile cible :"))
        self.blanc_contour_bleu(qp)
        qp.drawRect(260, 385 + 50, 120, 20)
        qp.drawRect(260, 435 + 50, 80, 20)
        qp.drawRect(260, 485 + 50, 300, 20)
        qp.drawRect(260, 535 + 50, 100, 20)
        self.noir(qp)
        qp.drawText(275, 400 + 50, QtCore.QString("88.95''N  15.10''O "))
        qp.drawText(275, 450 + 50, QtCore.QString("1.23539 V "))
        qp.drawText(275, 500 + 50, QtCore.QString("0.8245m, 0.23421m     68.35''S  1.36''O "))
        qp.drawText(275, 550 + 50, QtCore.QString("Ile A"))

    def setUpLiveVirtuel(self, qp):
        qp.drawPixmap(640, 0, QtGui.QPixmap("test_image7.png"),0, 90, 640, 480)
        qp.drawPixmap(640, 350, QtGui.QPixmap("test_image_vide.png"),0, 90, 640, 480)
        self.orange(qp)
        qp.drawRect(450, 348, 830, 5)
        qp.drawRect(638, 0, 5, 700)
        qp.drawText(450, 338, QtCore.QString("TEMPS REEL"))
        qp.drawText(450, 378, QtCore.QString("VIRTUEL"))


    def drawRectangles(self, qp):

        self.vert(qp)
        qp.drawRect(953, 457, 30, 30)

        self.bleu(qp)
        qp.drawRect(823, 578, 30, 30)



    def drawCircles(self, qp):
        self.rouge(qp)
        qp.drawEllipse(807, 442, 32, 32)

    def drawPolygones(self, qp):
        self.jaune(qp)
        self.polygone_init(qp, 900, 592)

    def drawTriangles(self, qp):
        self.jaune(qp)
        self.triangle_init(qp, 722, 568)

    def triangle_init(self, qp, x, y):
        polygone = QtGui.QPolygon([
            QtCore.QPoint(x+ 0, y + 36),
            QtCore.QPoint(x + 18, y + 0),
            QtCore.QPoint(x + 36, y + 36)
        ])
        qp.drawConvexPolygon(polygone)

    def polygone_init(self, qp, x, y):
        polygone = QtGui.QPolygon([
            QtCore.QPoint(x + 0, y + 18),
            QtCore.QPoint(x + 18, y),
            QtCore.QPoint(x + 36, y + 18),
            QtCore.QPoint(x + 27, y + 36),
            QtCore.QPoint(x + 9, y + 36),
            QtCore.QPoint(x + 0, y + 18)
        ])
        qp.drawConvexPolygon(polygone)

    def blanc_contour_bleu(self, qp):
        qp.setBrush(QtGui.QColor(250, 250, 250, 250))
        qp.setPen(QtGui.QColor(0, 0, 250))


    def noir(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 0, 250))
        qp.setPen(QtGui.QColor(0, 0, 0))

    def orange(self, qp):
        qp.setBrush(QtGui.QColor(252, 100, 0, 250))
        qp.setPen(QtGui.QColor(252, 100, 0))

    def jaune(self, qp):
        qp.setBrush(QtGui.QColor(205, 175, 0, 250))
        qp.setPen(QtGui.QColor(205, 175, 0))

    def rouge(self, qp):
        qp.setBrush(QtGui.QColor(140, 0, 30, 250))
        qp.setPen(QtGui.QColor(140, 0, 30))

    def vert(self, qp):
        qp.setBrush(QtGui.QColor(0, 110, 60, 250))
        qp.setPen(QtGui.QColor(0, 110, 60))

    def bleu(self, qp):
        qp.setBrush(QtGui.QColor(0, 140, 190, 250))
        qp.setPen(QtGui.QColor(0, 140, 190))

def main():

    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()