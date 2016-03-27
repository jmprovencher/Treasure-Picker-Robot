from PyQt4 import QtGui, QtCore

class RedirigeurTexte():
    def __init__(self, widget, tag):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        if self.tag == "stdout":
            self.widget.setTextColor(QtCore.Qt.green)
        elif self.tag == "stderr":
            self.widget.setTextColor(QtCore.Qt.red)
        self.widget.insertPlainText(str)
        c = self.widget.textCursor()
        c.movePosition(QtGui.QTextCursor.End)
        self.widget.setTextCursor(c)
