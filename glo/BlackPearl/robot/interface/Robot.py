# import the necessary packages
from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from threading import Thread, RLock
import time

verrou = RLock()

class Robot(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("Init")
        #self.uartDriver = uartDriver
        self.alignementTresor = False
        self.alignementDepot = False
        self.positionTresor = False
        self.positionDepot = False
        self.demarrerConnectionTCP()
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self)

    def run(self):
        print("Robot run..")

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.start()


    def demarrerConnectionTCP(self):
        self.robotClient = RobotClient(self)
        self.robotClient.start()

    def demarrerPhaseAlignement(self, typeAlignement):
        self.demarrerFeedVideo()
        time.sleep(2)
        if (typeAlignement == "depot"):
            self.alignementDepot = True
        else:
            self.alignementTresor = True
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement'):
            self.demarrerPhaseAlignement(parametre)
        else:
            print("Commande directe")
            #self.uartDriver.sendCommand(commande, parametre)