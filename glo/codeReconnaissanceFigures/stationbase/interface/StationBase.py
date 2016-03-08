# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
import ConfigPath


class StationBase():
    def __init__(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.imageVirtuelle = ImageVirtuelle((100,100))
        self.initialiserStationBase()

    def initialiserStationBase(self):
        self.analyseImageWorld.chargerImage(ConfigPath.Config().appendToProjectPath('images/table2/trajet1.png'))
        self.analyseImageWorld.trouverElementsCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.imageVirtuelle.ajouterIles(self.carte.listeIles)
        self.imageVirtuelle.ajouterTresors(self.carte.listeTresors)

        self.carte.afficherCarte()
        self.analyseImageWorld.dessinerElementCartographique()
        self.analyseImageWorld.afficherImage()

        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.analyseImageWorld.dessinerDebutFinTrajet((50, 50), (1500, 400))
        self.analyseImageWorld.afficherImage()
        self.carte.trajectoire.trouverTrajet((50, 50), (1500, 400))
        self.carte.trajectoire.afficherTrajectoire()  # Dans le terminal
        self.analyseImageWorld.dessinerTrajet(self.carte.trajectoire.trajectoire)  # Sur la photo
        self.analyseImageWorld.afficherImage()
