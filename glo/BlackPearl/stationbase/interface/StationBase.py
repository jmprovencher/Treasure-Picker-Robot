# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideoStation import FeedVideoStation
from stationbase.communication.TCPServer import TCPServer
from stationbase.interface.ImageVirtuelle2 import ImageVirtuelle2
import time
import cv2

class StationBase(object):
    def __init__(self):
        self.demarrerFeedVideo()
        self.carte = Carte()
        self.demarerAnalyseImageWorld()
        self.demarerImageVirtuelle()
        self.envoyerFichier = False
        #self.demarerConnectionTCP()
        self.demarerRoutine()
        self.destination = None
        self.trajectoireReel = None

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoStation()
        self.threadVideo.start()

    def demarerConnectionTCP(self):
        self.threadConnection = TCPServer(self)
        self.threadConnection.start()

    def demarerAnalyseImageWorld(self):
        time.sleep(1) #TODO: Verifier que la premiere capture est bel et bien effectue
        self.threadAnalyseImageWorld = AnalyseImageWorld(self)
        self.threadAnalyseImageWorld.start()

    def demarerImageVirtuelle(self):
        self.threadRafraichireImVirtuelle = ImageVirtuelle2(self)
        self.threadRafraichireImVirtuelle.start()

    def demarerRoutine(self):
        time.sleep(2) #TODO: Verifier que la premiere analise est bel et bien effectue
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.etapeStation()

    def identifierDestination(self, etape):
        if (etape == 'RECHARGE'):
            self.destination = self.carte.stationRecharge.getCentre()

    def etapeStation(self):
        self.identifierDestination('RECHARGE')
        #trajectoirePrevu = self.carte.trajectoire.trouverTrajet(self.carte.infoRobot.getCentre(), self.destination)
        #self.imageVirtuelle.dessinerTrajetPrevu(self.carte.infoRobot.getCentre(), self.destination, trajectoirePrevu)
        WtrajectoirePrevu = self.carte.trajectoire.trouverTrajet((100, 100), self.destination)
        #self.imageVirtuelle.dessinerTrajetPrevu((100, 100), self.destination, trajectoirePrevu)
        #self.trajectoireReel = trajectoirePrevu






