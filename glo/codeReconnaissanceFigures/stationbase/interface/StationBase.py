# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideo import FeedVideo
import ConfigPath



class StationBase(object):
    def __init__(self, feedVideo):
        self.analyseImageWorld = AnalyseImageWorld()
        self.feedVideo = feedVideo
        self.carte = Carte()
        self.initialiserStationBase()

    def analyserImage(self, imageCapture):
        self.imageReelle = imageCapture

        ###### ANALYSER IMAGE ICI AU LIEU DU PATH ######
        #self.analyseImageWorld.chargerImage(self.imageReelle)
        self.analyseImageWorld.chargerImage(ConfigPath.Config().appendToProjectPath('images/table3/trajet2.png'))

        self.analyseImageWorld.trouverElementsCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)

    def getImageReelle(self):
        return self.imageReelle

    def initialiserStationBase(self):
        self.feedVideo = FeedVideo()
        self.feedVideo.bind_to(self.analyserImage)

    def suspendreFeedVideo(self):
        self.feedVideo.suspendreCapture()

    def demarrerFeedVideo(self):
        self.feedVideo.demarrerCapture()

        #self.carte.afficherCarte()
        #self.analyseImageWorld.dessinerElementCartographique()
        #self.analyseImageWorld.afficherImage()
        #self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        #self.analyseImageWorld.dessinerDebutFinTrajet((100, 100), (1500, 400))
        #self.analyseImageWorld.afficherImage()
        #self.carte.trajectoire.trouverTrajet((100, 100), (1500, 400))
        #self.carte.trajectoire.afficherTrajectoire()  # Dans le terminal
        #self.analyseImageWorld.dessinerTrajet(self.carte.trajectoire.trajectoire)  # Sur la photo
        #self.analyseImageWorld.afficherImage()
