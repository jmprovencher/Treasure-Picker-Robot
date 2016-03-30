# import the necessary packages
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPainter
from PyQt4.QtCore import QString
from stationbase.interface.StationBase import StationBase
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
from stationbase.interface.AffichageDeBase import AffichageDeBase
from Tkinter import *
from stationbase.interface.RedirigeurTexte import RedirigeurTexte

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.initUI()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #self.affichageDeBase = AffichageDeBase(qp)
        #result = None
        #while result is None:
            #try:
                #result = self.threadStationBase.threadCommunication.robotEstPret
                #if(result):
                    #self.dessinerRobotActive(qp)
            #except:
                #pass
        qp.end()


    def initUI(self):
        self.setWindowTitle('Interface')
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.largeur = screenShape.width()
        self.hauteur = screenShape.height()
        self.resize(self.largeur, self.hauteur)
        self.setAutoFillBackground(False)
        self.feed = QLabel(self)
        self.buffer = 25
        self.feed.setGeometry(5, self.hauteur-(600+self.buffer+5), 800, 600)
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        self.orientation = QLabel(self)
        self.orientation.setGeometry(380, 22, 640, 50)
        self.position = QLabel(self)
        self.position.setGeometry(380, 52, 640, 80)
        #self.direction = QLabel(self)
        #self.direction.setGeometry(380, 52, 400, 80)

        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Debuter')
        self.btnDemarer.setGeometry(40, 25, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutineComplete)

        self.btnDepStation = QPushButton(self)
        self.btnDepStation.setText('Deplacement station')
        self.btnDepStation.setGeometry(40, 70, 200, 27)
        self.btnDepStation.clicked.connect(self.demarerDepStation)

        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Se charger')
        self.btnDemarer.setGeometry(40, 100, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Deplacement tresor')
        self.btnDemarer.setGeometry(40, 130, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Prendre tresor')
        self.btnDemarer.setGeometry(40, 160, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Deplacement ile cible')
        self.btnDemarer.setGeometry(40, 190, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnAliDepot = QPushButton(self)
        self.btnAliDepot.setText('Depot tresor')
        self.btnAliDepot.setGeometry(40, 220, 200, 27)
        self.btnAliDepot.clicked.connect(self.demarerAlignementIle)
        self.tensionCondensateur = QLabel(self)
        self.tensionCondensateur.setGeometry(380, 82, 640, 110)
        self.manchester = QLabel(self)
        self.manchester.setGeometry(380, 102, 640, 130)
        self.ileCible = QLabel(self)
        self.ileCible.setGeometry(380, 122, 640, 150)
        self.robotPretAffiche = QLabel(self)
        self.robotPretAffiche.setGeometry(380, 142, 640, 170)
        self.initTextBox()

    def demarerRoutineComplete(self):
        self.threadStationBase = StationBase('routine complete')
        self.demarerRoutine()

    def demarerDepStation(self):
        self.threadStationBase = StationBase('deplacement station')
        self.demarerRoutine()

    def demarerAlignementStation(self):
        self.threadStationBase = StationBase('alignement station')
        self.demarerRoutine()

    def demarerDepTresor(self):
        self.threadStationBase = StationBase('deplacement tresor')
        self.demarerRoutine()

    def demarerAlignementTresor(self):
        self.threadStationBase = StationBase('alignement tresor')
        self.demarerRoutine()

    def demarerDepIle(self):
        self.threadStationBase = StationBase('deplacement ile')
        self.demarerRoutine()

    def demarerAlignementIle(self):
        self.threadStationBase = StationBase('alignement ile')
        self.demarerRoutine()

    def demarerRoutine(self):
        self.threadStationBase.start()
        self.connect(self.threadAfficherImageVirtuelle, QtCore.SIGNAL("update()"), self.update_gui)
        self.threadAfficherImageVirtuelle.start()

    def update_gui(self):
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        #self.tensionCondensateur.setText(QString(self.threadStationBase.tensionCondensateur))
        QtGui.QApplication.processEvents()
        if(not self.threadStationBase.carte.infoRobot is None):
            self.position.setText(QString('Position du robot : ' + str(self.threadStationBase.carte.infoRobot.centre_x) + 'x ' + str(self.threadStationBase.carte.infoRobot.centre_y) +'y'))
            self.orientation.setText(QString('Orientation du robot : ' + str(self.threadStationBase.carte.infoRobot.orientation)+'\xb0'))
        self.feed.repaint()
        self.tensionCondensateur.setText(QString('Tension condensateur : ' + str(self.threadStationBase.tensionCondensateur) + 'V'))
        self.ileCible.setText(QString('Ile cible : ' + '?'))
        #self.ileCible.setText(QString('Ile cible : ' + self.threadStationBase.descriptionIleCible.forme + ' ' + self.threadStationBase.carte.cible.ileChoisie.forme.couleur)
        self.manchester.setText(QString('Manchester : ' + self.threadStationBase.manchester))
        if(self.threadStationBase.robotEstPret):
            self.robotPretAffiche(QString('Connecté'))
        else:
            self.robotPretAffiche(QString('Non Connecté'))
        self.robotPretAffiche.repaint()
        self.manchester.repaint()
        self.ileCible.repaint()
        self.orientation.repaint()
        self.position.repaint()
        self.tensionCondensateur.repaint()

    def dessinerRobotActive(self, qp):
        qp.setBrush(QtGui.QColor(0, 200, 120, 250))
        qp.setPen(QtGui.QColor(0, 200, 120))
        qp.drawEllipse(1005, 55, 40, 40)

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