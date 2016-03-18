# import the necessary packages
import sys

from robot.interface.Robot import Robot
from stationbase.interface.StationBase import StationBase
from stationbase.interface.ImageReelle import ImageReelle
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
from stationbase.interface.FeedVideoStation import FeedVideo
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter, QImage, QWidget

import ConfigPath


class Interface(QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')

    def paintEvent(self, e):
        qp2 = QPainter()
        qp2.begin(self)
        qp2.drawPixmap(640, 0, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('imageReelle.png')), 0, 90, 640, 480)
        qp2.end()
        self.update()


def main():

    app2 = QtGui.QApplication(sys.argv)
    interface2 = Interface()
    interface2.show()
    sys.exit(app2.exec_())


if __name__ == '__main__':
    main()
