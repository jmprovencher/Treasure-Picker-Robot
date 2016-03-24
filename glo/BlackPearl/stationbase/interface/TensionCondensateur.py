from PyQt4 import QtGui, QtCore
import cv2
import numpy as np
import time
from PyQt4.QtCore import QThread
import ConfigPath

class TensionCondensateur(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.tension = '?'

    def run(self):

        while 1:
            self.tension = '1.2'+'V'
            time.sleep(0.2)