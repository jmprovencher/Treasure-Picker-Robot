from PyQt4 import QtGui, QtCore
import sys
from stationbase.interface.Interface import Interface


def main():
    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())

main()
