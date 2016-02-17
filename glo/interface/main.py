import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window.resize(320,240)
window.setWindowTitle("Wazzzzappp")
btn = QtGui.QPushButton('Wazzzzappp', window)
btn.setToolTip('Click to quit!')
btn.clicked.connect(exit)
btn.resize(btn.sizeHint())
btn.move(100, 80)

window.show()

sys.exit(app.exec_())