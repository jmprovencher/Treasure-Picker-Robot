# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideoStation import FeedVideoStation
from stationbase.communication.StationServeur import StationServeur
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
        self.destination = None
        self.trajectoireReel = None
        self.trajectoirePrevue = None
        self.envoyerFichier = False
        #self.demarrerConnectionTCP()
        self.demarrerFeedVideo()
        self.carte = Carte()
        self.demarrerAnalyseImageWorld()
        self.demarrerImageVirtuelle()

    def run(self):
        self.demarerRoutine()

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoStation()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        self.threadCommunication = StationServeur(self)
        self.threadCommunication.start()

    def demarrerAnalyseImageWorld(self):
        self.threadAnalyseImageWorld = AnalyseImageWorld(self)
        self.threadAnalyseImageWorld.start()

    def demarrerImageVirtuelle(self):
        self.threadImageVirtuelle = ImageVirtuelle(self)
        self.threadImageVirtuelle.start()

    def demarerRoutine(self):
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.etapeStation()
        time.sleep(100000)

    def identifierDestination(self, etape):
        if (etape == 'RECHARGE'):
            self.destination = self.carte.stationRecharge.getCentre()

    def etapeStation(self):
        self.identifierDestination('RECHARGE')
        self.trajectoirePrevue = []
        #while 1:
        #    if (not self.carte.infoRobot is None):
        #        self.trajectoirePrevue = self.carte.trajectoire.trouverTrajet(self.carte.infoRobot.getCentre(), self.destination)
        #        break
            #time.sleep(1)







