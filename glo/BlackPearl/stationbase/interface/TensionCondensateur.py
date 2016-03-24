from PyQt4 import QtGui, QtCore
import cv2
import numpy as np
import time
from threading import Thread
import ConfigPath

class TensionCondensateur(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.tension = '?'
        self.tensionInt = 1

    def run(self):
        while 1:
            self.tensionInt += 1
            self.tension = str(self.tensionInt)+'V'
            print(self.tension)
            time.sleep(1)