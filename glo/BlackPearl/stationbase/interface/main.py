# import the necessary packages
import sys

from robot.interface.Robot import Robot
from stationbase.interface.AffichageDeBase import AffichageDeBase
from stationbase.interface.StationBase import StationBase
from stationbase.interface.ImageReelle import ImageReelle
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
from stationbase.interface.FeedVideoStation import FeedVideo
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter

import ConfigPath


class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')
        self.btnDemarrer = QtGui.QPushButton('Demarrer', self)
        #self.btnVideo = QtGui.QPushButton('Start Video', self)
        self.btnDemarrer.resize(120, 46)
        #self.btnVideo.resize(120, 46)
        self.btnDemarrer.move(200, 200)
        #self.btnVideo.move(200, 300)
        self.ilesDetectees = []
        self.tresorsDetectes = []
        self.trajectoire = []
        self.btnDemarrer.clicked.connect(self.demarrerRoutine)
        #self.btnVideo.clicked.connect(self.demarrerCapture)
        self.demarre = False

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        print(self.demarre)
        if (self.demarre):
            print("Paint event")
            image = self.obtenirImageReelle()
            self.imageReelle = ImageReelle(image)
            self.trajectoire = self.stationBase.getCarte()
            imageVirtuelle = ImageVirtuelle(qp, self.ilesDetectees, self.tresorsDetectes, self.trajectoire)

        self.affichageDeBase = AffichageDeBase(qp)
        qp.end()

    #Cette fonction est automatiquement appelee quand l'image est updater dans stationBase
    def dessinerImageReelle(self, qp):
        image = self.obtenirImageReelle()
        #self.imageReelle.updateImage(image)
        print("Essaye de dessiner....")

    def obtenirImageReelle(self):
        return self.stationBase.getImageReelle()

    def demarrerRoutine(self):
        self.feed = FeedVideo()
        self.stationBase = StationBase(self.feed)
        self.stationBase.bind_to(self.dessinerImageReelle)

    #def demarrerCapture(self):
        self.fun = self.stationBase.feedVideo.demarrerCapture()
        self.ilesDetectees = self.stationBase.carte.listeIles
        self.tresorsDetectes = self.stationBase.carte.listeTresors
        self.demarre = True
        #self.repaint()

def main():

    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
