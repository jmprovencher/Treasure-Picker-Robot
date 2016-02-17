import sys
from PyQt4 import QtGui
import timeit


class RobotUI(QtGui.QWidget):

    def __init__(self):
        super(RobotUI, self).__init__()
        self.champ_textbox = QtGui.QLineEdit(self)
        self.champ_textbox = QtGui.QLineEdit(self)
        self.champ_textbox.move(140, 20)
        self.champ_textbox.resize(120, 20)
        self.initUI()

    def updateTextBox(self):
        self.champ_textbox.setText(str(timeit.timeit()))
        self.champ_textbox.update()

    def initUI(self):
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
    robUI = RobotUI()
    sys.exit(app.exec_())
    while 1:
        robUI.updateTextBox()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()

