import sys
from PyQt4 import QtGui, QtCore
import timeit


class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        timer = QtCore.QTimer
        self.champ_textbox = QtGui.QLineEdit(self)
        self.champ_textbox = QtGui.QLineEdit(self)
        self.champ_textbox.move(140, 20)
        self.champ_textbox.resize(120, 20)
        champ = QtGui.QLabel('Champ')
        champ.move(20, 2)


        btn = QtGui.QPushButton('Bouton 3', self)
        btn.setToolTip('Click to quit!')
        btn.clicked.connect(exit)
        btn.resize(btn.sizeHint())
        btn.move(20, 300)

        btn2 = QtGui.QPushButton('Bouton 2', self)
        btn2.setToolTip('Click to quit!')
        btn2.clicked.connect(exit)
        btn2.resize(btn.sizeHint())
        btn2.move(20, 350)

        btn3 = QtGui.QPushButton('Bouton 1', self)
        btn3.setToolTip('Click to quit!')
        btn3.clicked.connect(exit)
        btn3.resize(btn.sizeHint())
        btn3.move(20, 400)

        self.resize(720,490)
        self.setWindowTitle('Design 3')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())
if __name__ == '__main__':
    main()