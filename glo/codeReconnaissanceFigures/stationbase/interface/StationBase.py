# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld

class StationBase():

    def __init__(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.initialiserStationBase()

    def initialiserStationBase(self):
        self.analyseImageWorld.chargerImage('Image/table2/trajet1.png')
        self.analyseImageWorld.trouverElementCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.afficherCarte()
        self.analyseImageWorld.dessinerElementCartographique()
        self.analyseImageWorld.afficherImage()

        # Trouver et afficher le trajet
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        self.analyseImageWorld.dessinerDebutFinTrajet((50, 50),(1500, 400))
        self.analyseImageWorld.afficherImage()
        self.carte.trajectoire.trouverTrajet((50, 50),(1500, 400))
        self.carte.trajectoire.afficherTrajectoire()                            # Dans le terminal
        self.analyseImageWorld.dessinerTrajet(self.carte.trajectoire.trajectoire)    # Sur la photo
        self.analyseImageWorld.afficherImage()