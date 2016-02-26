# import the necessary packages
from elements.ElementCartographique import ElementCartographique

class Ile(ElementCartographique):

    def __init__(self, centre, couleur, forme):
        self.centre_x, self.centre_y = centre
        self.couleur = couleur
        self.forme = forme

    def afficher(self):
        print "ILE"
        print "%s %s" % (self.forme, self.couleur)
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print "---------------------------------------------------"
