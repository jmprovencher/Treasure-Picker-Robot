# import the necessary packages
from elements.ElementCartographique import ElementCartographique
from elements.Ile import Ile

class Cible():
    def __init__(self, carte, indice):
        self.carte = carte
        self.indice = indice
        self.tresorChoisi = None
        self.ileChoisie = None
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







