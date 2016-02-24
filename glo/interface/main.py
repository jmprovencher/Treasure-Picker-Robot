import sys
from PyQt4 import QtGui, QtCore

class Interface(QtGui.QWidget):

    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawPixmap(640, 0, QtGui.QPixmap("test_image7.png"),0, 90, 640, 480)
        qp.drawPixmap(640, 350, QtGui.QPixmap("test_image7.png"),0, 90, 640, 480)
        self.drawRectangles(qp)
        self.drawCircles(qp)
        self.drawPolygones(qp)
        self.drawTriangles(qp)
        qp.end()



    def drawRectangles(self, qp):

        self.vert(qp)
        qp.drawRect(1000, 600, 20, 20)

        self.bleu(qp)
        qp.drawRect(250, 15, 20, 20)



    def drawCircles(self, qp):
        self.rouge(qp)
        qp.drawEllipse(10, 10, 20, 20)

    def drawPolygones(self, qp):
        self.jaune(qp)
        polygone = QtGui.QPolygon([
            QtCore.QPoint(800, 60),
            QtCore.QPoint(814, 46),
            QtCore.QPoint(828, 60),
            QtCore.QPoint(821, 74),
            QtCore.QPoint(807, 74),
            QtCore.QPoint(800, 60)
        ])
        qp.drawConvexPolygon(polygone)

    def drawTriangles(self, qp):
        self.jaune(qp)
        polygone = QtGui.QPolygon([
            QtCore.QPoint(850, 60),
            QtCore.QPoint(862, 36),
            QtCore.QPoint(874, 60)
        ])
        qp.drawConvexPolygon(polygone)


    def jaune(self, qp):
        qp.setBrush(QtGui.QColor(200, 200, 0, 200))
        qp.setPen(QtGui.QColor(200, 200, 0))

    def rouge(self, qp):
        qp.setBrush(QtGui.QColor(200, 0, 0, 200))
        qp.setPen(QtGui.QColor(200, 0, 0))

    def vert(self, qp):
        qp.setBrush(QtGui.QColor(0, 200, 0, 160))
        qp.setPen(QtGui.QColor(0, 200, 0))

    def bleu(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 200, 200))
        qp.setPen(QtGui.QColor(0, 0, 200))

def main():

    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()