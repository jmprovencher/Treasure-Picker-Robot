# import the necessary packages
import sys
from stationbase.interface.AffichageDeBase import AffichageDeBase
from stationbase.interface.StationBase import StationBase
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter
import time

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')
        self.btnDemarrer = QtGui.QPushButton('Demarrer', self)
        self.btnDemarrer.resize(120, 46)
        self.btnDemarrer.move(200, 200)
        self.btnDemarrer.clicked.connect(self.demarrerRoutine)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #print(self.demarre)
        #if (self.demarre):
        #    print("Paint event")
        #    image = self.obtenirImageReelle()
        #    self.imageReelle = ImageReelle(image)
        #    self.trajectoire = self.stationBase.getCarte()
        #    imageVirtuelle = ImageVirtuelle(qp, self.ilesDetectees, self.tresorsDetectes, self.trajectoire)
        self.affichageDeBase = AffichageDeBase(qp)
        self.threadStationBase.threadVideo.
        qp.drawPixmap(640, 0, QtGui.QPixmap(self.imageCamera), 0, 90, 640, 480)
        qp.end()

    #Cette fonction est automatiquement appelee quand l'image est updater dans stationBase
    def dessinerImageReelle(self, qp):
        image = self.obtenirImageReelle()
        #self.imageReelle.updateImage(image)
        print("Essaye de dessiner....")

    def obtenirImageReelle(self):
        return self.stationBase.getImageReelle()



    def demarrerRoutine(self):
        self.threadStationBase = StationBase()
        time.sleep(5)
        self.threadStationBase.start()

def main():

    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
