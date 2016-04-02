# import the necessary packages
from elements.ElementCartographique import ElementCartographique
from elements.Ile import Ile
import copy

class Cible():
    def __init__(self, args):
        self.carte = args[0]
        if (len(args) == 1):
            self.ileChoisie = None
            self.tresorChoisi = None
            self.indice = 'Carre'
        else:
            self.indice = args[1]
            self.trouverIleCible()

    def trouverIleCible(self, pos):
        pos = copy.deepcopy(pos)
        ilesPotentielle = self.carte.getIlesIndice(self.indice)
        distanceMin = 1000000
        for tresor in self.carte.listeTresors:
            distance = 0
            trajetTresor = self.carte.trajectoire.trouverTrajet(pos, tresor.getCentre())
            distanceTresor = self.carte.trajectoire.trouverLongueurTrajetPixCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.trajectoire.trouverTrajet(pos, tresor.getCentre())
                distanceIle = self.carte.trajectoire.trouverLongueurTrajetPixCarre(trajetIle)
                distanceTotale = distanceTresor + distanceIle
                if (distanceMin > distanceTotale):
                    distanceMin = distanceTotale
                    self.tresorChoisi = tresor
                    self.ileChoisie = ile







