from elements.ElementCartographique import ElementCartographique


class Tresor(ElementCartographique):
    def __init__(self, centre):
        self.centre_x, self.centre_y = centre
        self.forme = "Station"

    def afficher(self):
        print "Station"
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print "---------------------------------------------------"
