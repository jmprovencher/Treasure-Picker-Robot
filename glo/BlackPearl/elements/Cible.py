# import the necessary packages
from elements.ElementCartographique import ElementCartographique
from elements.Ile import Ile

class Cible():
    def __init__(self, carte, couleur, forme):
        self.centre_x, self.centre_y = centre
        self.couleur = couleur
        self.forme = forme

    def afficher(self):
        print "ILE"
        print "%s %s" % (self.forme, self.couleur)
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print "---------------------------------------------------"
