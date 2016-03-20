# import the necessary packages
from elements.Carte import Carte
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from robot.communication.TCPClient import TCPClient
import ConfigPath


class Robot(object):
    def __init__(self):
        self.phaseAlignement = False
        self.positionTresor = False
        self.positionDepot = True
        #monClient = TCPClient()
        self.analyseImageEmbarquee = AnalyseImageEmbarquee()


    def analyserImage(self, imageCapture):
        print("Analyzing robot image")
        self.analyseImageEmbarquee.chargerImage(imageCapture)
        #self.analyseImageEmbarquee.chargerImage(ConfigPath.Config().appendToProjectPath('images/camera_robot/iles/test_image15.png'))
        if (self.positionDepot == True):
            self.analyseImageEmbarquee.evaluerPositionDepot("Rouge")
            #self.analyseImageEmbarquee.alignementIle.afficherFeed()
        elif (self.positionTresor == True):
            self.analyseImageEmbarquee.evaluerPositionTresor()

    def debuterPhaseAlignement(self):
        self.phaseAlignement = True
        self.initialiserVideo()

    def initialiserVideo(self):
        self.feedVideo = FeedVideoRobot()
        self.feedVideo.bind_to(self.analyserImage)

    def suspendreFeedVideo(self):
        self.feedVideo.suspendreCapture()

    def demarrerFeedVideo(self):
        self.feedVideo.demarrerCapture()
