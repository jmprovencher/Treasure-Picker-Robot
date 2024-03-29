from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import QString
from stationbase.interface.StationBase import StationBase
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
from Tkinter import *
from stationbase.interface.RedirigeurTexte import RedirigeurTexte
from timeit import default_timer
import math

MAX_TEMPS = 10

duration = default_timer()


class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadStationBase = None
        self.initUI()
        self.threadAfficherImageVirtuelle.start()
        self.infoTemps = 0
        self.infoTempsIndice = True


    def initUI(self):
        self.initGeneral()
        self.initButtons()
        self.initInfo()
        self.initTextBox()


    def update_gui(self):
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        QtGui.QApplication.processEvents()
        self.feed.repaint()
        if self.threadStationBase.getCarte().getRobot() is not None:
            self.rechargerInfo(self.position, 'Position du robot : ' +
                               str(self.threadStationBase.getCarte().getRobot().getX()) + 'x ' +
                               str(self.threadStationBase.getCarte().getRobot().getY()) + 'y')
            self.rechargerInfo(self.orientation, 'Orientation du robot : ' +
                               str(self.threadStationBase.getCarte().getRobot().getOrientation()) + '\xb0')
        self.rechargerInfo(self.tensionCondensateur, 'Tension condensateur : ' +
                           str(self.threadStationBase.getTensionCondensateur()) + 'V')
        if self.threadStationBase.getCarte().getCible() is not None:
            self.rechargerInfo(self.ileCible, 'Ile cible : ' + self.threadStationBase.getCarte().getCible().getIndice())
        self.rechargerInfo(self.manchester, 'Manchester : ' + self.threadStationBase.getManchester())
        if self.threadStationBase.threadCommunication.getRobotPret():
            self.rechargerInfoCouleur(self.robotPretAffiche, 'Connecte', 'green')
        if self.threadStationBase is not None:
            if not self.threadStationBase.roundTerminee:
                tempsTotal = self.infoTemps + default_timer() - self.threadStationBase.startTimer
                secondeTotal = math.floor(tempsTotal - math.floor(tempsTotal/60)*60)
                minuteTotal = math.floor(tempsTotal/60)
                if secondeTotal < MAX_TEMPS:
                    stringSeconde = '0' + str(int(secondeTotal))
                else:
                    stringSeconde = str(int(secondeTotal))
                if minuteTotal == 0:
                    stringMinute = ' 0'
                elif minuteTotal < MAX_TEMPS:
                    stringMinute = ' ' + str(int(minuteTotal))
                else:
                    stringMinute = str(minuteTotal)
                self.rechargerInfoCouleur(self.tempsDepuisDemarrer, '  ' + stringMinute + ':' + stringSeconde, 'blue')
            else:
                if not self.infoTempsIndice:
                    self.infoTemps += default_timer() - self.threadStationBase.startTimer
                    self.infoTempsIndice = True

    def initGeneral(self):
        self.setWindowTitle('Interface')
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.largeur = screenShape.width()
        self.hauteur = screenShape.height()
        self.resize(self.largeur, self.hauteur)
        self.setAutoFillBackground(False)
        self.feed = QLabel(self)
        self.buffer = 25
        self.numeroTable = 2
        self.feed.setGeometry(5, self.hauteur-(600+self.buffer+5), 800, 600)
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)

    def initInfo(self):
        self.orientation = self.afficherInitInfo(380, 42, 640, 50, 'Orientation du robot : ?')
        self.position = self.afficherInitInfo(380, 62, 640, 80, 'Position du robot : ?')
        self.tensionCondensateur = self.afficherInitInfo(380, 82, 640, 110, 'Tension condensateur : ?')
        self.manchester = self.afficherInitInfo(380, 102, 640, 130, 'Manchester : ?')
        self.ileCible = self.afficherInitInfo(380, 122, 640, 150, 'Ile cible : ?')
        self.robotNonActif = self.afficherInitInfo(380, 142, 640, 170, 'Robot :')
        self.robotPretAffiche = self.afficherInitInfoCouleur(444, 142, 660, 170, 'Non Connecte', 'red')
        self.tempsDepuisDemarrerStatic = self.afficherInitInfo(380, 172, 640, 200, 'Temps : ')
        self.tempsDepuisDemarrerStatic.setFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold))
        self.tempsDepuisDemarrer = self.afficherInitInfo(494, 172, 740, 200, '    0:00')
        self.tempsDepuisDemarrer.setFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold))

    def initButtons(self):
        self.btnTable1 = self.afficherInitBouttons(40, 10, 100, 27, 'Table 1', self.setTable1)
        self.btnTable2 = self.afficherInitBouttons(140, 10, 100, 27, 'Table 2', self.setTable2)
        self.btnTable3 = self.afficherInitBouttons(240, 10, 100, 27, 'Table 3', self.setTable3)
        self.btnTable5 = self.afficherInitBouttons(340, 10, 100, 27, 'Table 5', self.setTable5)
        self.btnTable6 = self.afficherInitBouttons(440, 10, 100, 27, 'Table 6', self.setTable6)
        self.btnDemarer = self.afficherInitBouttons(40, 40, 200, 27, 'Debuter', self.demarerRoutine)

    def initTextBox(self):
        self.text = QtGui.QTextEdit(self)
        self.text.setGeometry(self.feed.frameGeometry().width()+10, 5, self.largeur-(5+self.feed.frameGeometry().width()+10), self.hauteur-(self.buffer+10))
        self.text.setReadOnly(True)
        self.text.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        font = self.text.font()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.text.moveCursor(QtGui.QTextCursor.End)
        self.text.setCurrentFont(font)
        sb = self.text.verticalScrollBar()
        sb.setValue(sb.maximum())
        self.text.ensureCursorVisible()
        pal = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        pal.setColor(QtGui.QPalette.Base, bgc)
        self.text.setPalette(pal)
        self.text.setTextColor(QtCore.Qt.white)
        self.text.insertPlainText('Black Pearl\n')
        sys.stdout = RedirigeurTexte(self.text, "stdout")
        sys.stderr = RedirigeurTexte(self.text, "stderr")

    def rechargerInfo(self, label, texte):
        label.setText(QString(texte))
        label.repaint()

    def rechargerInfoCouleur(self, label, texte, couleur):
        label.setText(QString(texte))
        label.setStyleSheet('color: ' + couleur)
        label.repaint()

    def afficherInitInfo(self, x, y, dimensionX, dimensionY, texte):
        info = QLabel(self)
        info.setGeometry(x, y, dimensionX, dimensionY)
        info.setText(QString(texte))
        return info

    def afficherInitInfoCouleur(self, x, y, dimensionX, dimensionY, texte, couleur):
        info = QLabel(self)
        info.setGeometry(x, y, dimensionX, dimensionY)
        info.setText(QString(texte))
        info.setStyleSheet('color: ' + couleur)
        return info

    def afficherInitBouttons(self, x, y, dimensionX, dimensionY, texte, connection):
        button = QPushButton(self)
        button.setText(texte)
        button.setGeometry(x, y, dimensionX, dimensionY)
        button.clicked.connect(connection)

    def setTable1(self):
        self.numeroTable = 1
        print('Vous avez choisi la Table ' + str(self.numeroTable))

    def setTable2(self):
        self.numeroTable = 2
        print('Vous avez choisi la Table ' + str(self.numeroTable))

    def setTable3(self):
        self.numeroTable = 3
        print('Vous avez choisi la Table ' + str(self.numeroTable))

    def setTable5(self):
        self.numeroTable = 5
        print('Vous avez choisi la Table ' + str(self.numeroTable))

    def setTable6(self):
        self.numeroTable = 6
        print('Vous avez choisi la Table ' + str(self.numeroTable))

    def demarerRoutine(self):
        self.threadStationBase = StationBase(self.numeroTable)
        self.threadStationBase.start()
        self.infoTempsIndice = False
        self.connect(self.threadAfficherImageVirtuelle, QtCore.SIGNAL("update()"), self.update_gui)
