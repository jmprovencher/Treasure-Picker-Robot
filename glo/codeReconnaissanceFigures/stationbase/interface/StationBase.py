# import the necessary packages
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld


class StationBase():

    def __init__(self):
        # self.analyseImageWorld = AnalyseImageWorld()
        # self.carte = Carte()
        self.main()

    def main(self):
        listNom = ['Image/table2/trajet1.png']#,'Image/table2/detection2.png','Image/table2/trajet1.png','Image/table2/trajet2.png','Image/table2/testVert1.png']

        for nom in listNom:

            # init
            self.analyseImageWorld = AnalyseImageWorld(nom)
            self.carte = Carte()

            # Trouver et afficher les elements
            self.analyseImageWorld.trouverElementCartographiques()
            self.carte.ajouterElementCarto(self.analyseImageWorld.elementsCartographiques)
            self.carte.afficherCarte()                                              # Dans le termianal
            self.analyseImageWorld.dessinerElementCartographique()                  # Sur la photo
            self.analyseImageWorld.afficherImage()

            # Trouver et afficher le trajet
            self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)
            self.analyseImageWorld.dessinerDebutFinTrajet((50, 50),(1500, 400))
            self.analyseImageWorld.afficherImage()
            self.carte.trajectoire.trouverTrajet((50, 50),(1500, 400))
            self.carte.trajectoire.afficherTrajectoire()                            # Dans le terminal
            self.analyseImageWorld.dessinerTrajet(self.carte.trajectoire.trajet)    # Sur la photo
            self.analyseImageWorld.afficherImage()


