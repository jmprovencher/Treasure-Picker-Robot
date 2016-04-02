# import the necessary packages
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import QString
from stationbase.interface.StationBase import StationBase
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
from Tkinter import *
from stationbase.interface.RedirigeurTexte import RedirigeurTexte

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.initUI()

    def initUI(self):
        self.initGeneral()
        self.initButtons()
        self.initInfo()
        self.initTextBox()

    def update_gui(self):
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        self.tensionCondensateur.setText(QString(self.threadStationBase.tensionCondensateur))
        QtGui.QApplication.processEvents()
        self.feed.repaint()
        if self.threadStationBase.getCarte().getRobot() is not None:
            self.position.rechargerInfo('Position du robot : ' +
                                        str(self.threadStationBase.getCarte().getRobot().getX()) + 'x ' +
                                        str(self.threadStationBase.getCarte().getRobot().getY()) + 'y')
            self.orientation.rechargerInfo('Orientation du robot : ' +
                                           str(self.threadStationBase.getCarte().getRobot().getOrientation()) + '\xb0')
        self.tensionCondensateur.rechargerInfo('Tension condensateur : '
                                               + str(self.threadStationBase.getTensionCondensateur()) + 'V')
        if self.threadStationBase.getCarte().getCible() is not None:
            self.ileCible.rechargerInfo('Ile cible : ' + self.threadStationBase.getCarte().getCible().getIndice())
        self.manchester.rechargerInfo('Manchester : ' + self.threadStationBase.getManchester())
        if self.threadStationBase.robotEstPret:
            self.rechargerInfoCouleur('Connecte', 'color: green')

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
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)

    def initInfo(self):
        self.orientation = self.afficherInitInfo(380, 42, 640, 50, 'Orientation du robot : ?')
        self.position = self.afficherInitInfo(380, 62, 640, 80, 'Position du robot : ?')
        self.tensionCondensateur = self.afficherInitInfo(380, 82, 640, 110, 'Tension condensateur : ?')
        self.manchester = self.afficherInitInfo(380, 102, 640, 130, 'Manchester : ?')
        self.ileCible = self.afficherInitInfo(380, 122, 640, 150, 'Ile cible : ?')
        self.robotNonActif = self.afficherInitInfo(380, 142, 640, 170, 'Robot :')
        self.robotPretAffiche = self.afficherInitInfoCouleur(444, 142, 660, 170, 'Non Connecte', 'red')

    def initButtons(self):
        self.btnTable1 = self.afficherInitBouttons(40, 10, 100, 27, 'Table 1', self.setTable1)
        self.btnTable2 = self.afficherInitBouttons(140, 10, 100, 27, 'Table 2', self.setTable2)
        self.btnTable3 = self.afficherInitBouttons(240, 10, 100, 27, 'Table 3', self.setTable3)
        self.btnTable5 = self.afficherInitBouttons(340, 10, 100, 27, 'Table 5', self.setTable5)
        self.btnTable6 = self.afficherInitBouttons(440, 10, 100, 27, 'Table 6', self.setTable6)
        self.btnDemarer = self.afficherInitBouttons(40, 40, 200, 27, 'Debuter', self.demarerRoutineComplete)
        self.btnDepStation = self.afficherInitBouttons(40, 70, 200, 27, 'Deplacement station', self.demarerDepStation)
        self.btnAliStation = self.afficherInitBouttons(40, 100, 200, 27, 'Alignement station', self.demarerAlignementStation)
        self.btnDepTresor = self.afficherInitBouttons(40, 130, 200, 27, 'Deplacement tresor', self.demarerDepTresor)
        self.btnAliTresor = self.afficherInitBouttons(40, 160, 200, 27, 'Alignement tresor', self.demarerAlignementTresor)
        self.btnDepIle = self.afficherInitBouttons(40, 190, 200, 27, 'Deplacement ile', self.demarerDepIle)
        self.btnAliIle = self.afficherInitBouttons(40, 220, 200, 27, 'Alignement ile', self.demarerAlignementIle)

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
        #sys.stdout = RedirigeurTexte(self.text, "stdout")
        #sys.stderr = RedirigeurTexte(self.text, "stderr")

    def rechargerInfo(self, texte):
        self.setText(QString(texte))
        self.repaint()

    def rechargerInfoCouleur(self, texte, couleur):
        self.setStyleSheet('color: ' + couleur)
        self.setText(QString(texte))
        self.repaint()

    def afficherInitInfo(self, x, y, dimensionX, dimensionY, texte):
        info = QLabel(self)
        info.setGeometry(x, y, dimensionX, dimensionY)
        return info.setText(QString(texte))

    def afficherInitInfoCouleur(self, x, y, dimensionX, dimensionY, texte, couleur):
        info = QLabel(self)
        info.setGeometry(x, y, dimensionX, dimensionY)
        info.setText(QString(texte))
        info.setStyleSheet('color: ' + couleur)

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

    def demarerRoutineComplete(self):
        self.threadStationBase = StationBase('routine complete', self.numeroTable)
        self.demarerRoutine()

    def demarerDepStation(self):
        self.threadStationBase = StationBase('deplacement station', self.numeroTable)
        self.demarerRoutine()

    def demarerAlignementStation(self):
        self.threadStationBase = StationBase('alignement station', self.numeroTable)
        self.demarerRoutine()

    def demarerDepTresor(self):
        self.threadStationBase = StationBase('deplacement tresor', self.numeroTable)
        self.demarerRoutine()

    def demarerAlignementTresor(self):
        self.threadStationBase = StationBase('alignement tresor', self.numeroTable)
        self.demarerRoutine()

    def demarerDepIle(self):
        self.threadStationBase = StationBase('deplacement ile', self.numeroTable)
        self.demarerRoutine()

    def demarerAlignementIle(self):
        self.threadStationBase = StationBase('alignement ile', self.numeroTable)
        self.demarerRoutine()

    def demarerRoutine(self):
        self.threadStationBase.start()
        self.connect(self.threadAfficherImageVirtuelle, QtCore.SIGNAL("update()"), self.update_gui)
        self.threadAfficherImageVirtuelle.start()
