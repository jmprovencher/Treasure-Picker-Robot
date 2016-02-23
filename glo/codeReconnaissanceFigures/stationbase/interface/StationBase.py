# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld


class StationBase():

    def __init__(self):
        self.analyseImageWorld = AnalyseImageWorld()
        self.carte = Carte()
        self.main()

    def main(self):
        # Trouver et afficher les elements
        self.analyseImageWorld.trouverElementCartographiques()
        self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
        self.carte.afficherCarte()                                              # Dans le termianal
        self.analyseImageWorld.dessinerElementCartographique()                  # Sur la photo
        self.analyseImageWorld.afficherImage()

        # # Trouver et afficher le trajet
        # self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
        # self.carte.trajectoire.trouverTrajet((50, 50),(1500, 400))
        # self.carte.trajectoire.afficherTrajectoire()                            # Dans le terminal
        # self.analyseImageWorld.dessinerTrajet(self.carte.trajectoire.trajet)    # Sur la photo
        # self.analyseImageWorld.afficherImage()


