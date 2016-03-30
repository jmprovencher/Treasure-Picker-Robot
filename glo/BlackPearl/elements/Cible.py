# import the necessary packages
from elements.ElementCartographique import ElementCartographique
from elements.Ile import Ile

class Cible():
    def __init__(self, args):
        self.carte = args[0]
        if (len(args) == 1):
            self.ileChoisie = None
            self.tresorChoisi = None
        else:
            self.indice = args[1]
            self.trouverIleCible()

    def trouverIleCible(self):
        ilesPotentielle = self.carte.getIles(self.indice)
        distanceMin = 1000000
        for tresor in self.carte.listeTresors:
            distance = 0
            trajetTresor = self.carte.trajectoire.trouverTrajet(self.carte.stationRecharge.getCentre(), self.tresor.getCentre())
            distanceTresor = self.carte.trajectoire.trouverLongueurTrajetPixCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.trajectoire.trouverTrajet(self.carte.stationRecharge.getCentre(), self.tresor.getCentre())
                distanceIle = self.carte.trajectoire.trouverLongueurTrajetPixCarre(trajetIle)
                distanceTotale = distanceTresor + distanceIle
                if (distanceMin > distanceTotale):
                    distanceMin = distanceTotale
                    self.tresorChoisi = tresor
                    self.ileChoisie = ile







