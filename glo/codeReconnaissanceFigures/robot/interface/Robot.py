# import the necessary packages
from elements.Carte import Carte
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
import ConfigPath


class Robot(object):
    def __init__(self):
        self.phaseAlignement = False
        self.positionTresor = False
        self.positionDepot = True
        self.analyseImageEmbarquee = AnalyseImageEmbarquee()
        #self.feedVideo = feedVideo
        self.carte = Carte()

    def analyserImage(self):
        #self.imageReelle = imageCapture
        ###### ANALYSER IMAGE ICI AU LIEU DU PATH ######
        # self.analyseImageWorld.chargerImage(self.imageReelle)
        self.analyseImageEmbarquee.chargerImage(ConfigPath.Config().appendToProjectPath('images/camera_robot/iles/test_image13.png'))
        if (self.positionDepot == True):
            self.analyseImageEmbarquee.evaluerPositionDepot("Vert")
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
