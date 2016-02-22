# import the necessary packages
from stationbase.vision.ElementCartographique import ElementCartographique


class Tresor(ElementCartographique):

    def __init__(self, centre):
        self.centre_x, self.centre_y = centre
        self.forme = "TRESOR"

    def afficher(self):
        print "TRESOR"
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print "---------------------------------------------------"
