# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
import ConfigPath


class StationBase():
    def __init__(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.initialiserStationBase()

    def initialiserStationBase(self):
        self.analyseImageWorld.chargerImage(ConfigPath.Config().appendToProjectPath('images/table3/trajet2.png'))
        self.analyseImageWorld.trouverElementsCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.afficherCarte()
        self.analyseImageWorld.dessinerElementCartographique()
        self.analyseImageWorld.afficherImage()

        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.analyseImageWorld.dessinerDebutFinTrajet((100, 100), (1500, 400))
        self.analyseImageWorld.afficherImage()
        self.carte.trajectoire.trouverTrajet((100, 100), (1500, 400))
        self.carte.trajectoire.afficherTrajectoire()  # Dans le terminal
        self.analyseImageWorld.dessinerTrajet(self.carte.trajectoire.trajectoire)  # Sur la photo
        self.analyseImageWorld.afficherImage()
