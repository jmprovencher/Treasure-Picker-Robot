# import the necessary packages
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import sys
import ConfigPath
from stationbase.interface.Interface import Interface

def main():
    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())

main()
