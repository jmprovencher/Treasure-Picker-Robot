# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideoStation import FeedVideoStation
from stationbase.communication.Communication import Communication
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
import time
import sys
from threading import Thread, RLock
import time
import cv2

verrou = RLock()

class StationBase(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.demarrerFeedVideo()
        self.carte = Carte()
        self.trajectoirePrevue = None
        self.demarerAnalyseImageWorld()
        self.demarerImageVirtuelle()
        self.envoyerFichier = False
        #self.demarerConnectionTCP()
        self.destination = None
        self.trajectoireReel = None

    def run(self):
        self.demarerRoutine()

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoStation()
        self.threadVideo.start()

    def demarerConnectionTCP(self):
        self.threadCommunication = Communication(self)
        self.threadCommunication.start()

    def demarerAnalyseImageWorld(self):
        time.sleep(5) #TODO: Verifier que la premiere capture est bel et bien effectue
        self.threadAnalyseImageWorld = AnalyseImageWorld(self)
        self.threadAnalyseImageWorld.start()

    def demarerImageVirtuelle(self):
        self.threadRafraichireImVirtuelle = ImageVirtuelle(self)
        self.threadRafraichireImVirtuelle.start()

    def demarerRoutine(self):
        time.sleep(5) #TODO: Verifier que la premiere analise est bel et bien effectue
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.etapeStation()

    def identifierDestination(self, etape):
        if (etape == 'RECHARGE'):
            self.destination = self.carte.stationRecharge.getCentre()

    def etapeStation(self):
        self.identifierDestination('RECHARGE')
        #self.trajectoirePrevue = self.carte.trajectoire.trouverTrajet(self.carte.infoRobot.getCentre(), self.destination)
        self.trajectoirePrevue = []






