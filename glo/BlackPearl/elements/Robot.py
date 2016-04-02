# import the necessary packages
from elements.ElementCartographique import ElementCartographique

class Robot(ElementCartographique):
    def __init__(self, centre, orientation):
        self.centre_x, self.centre_y = centre
        self.orientation = orientation
        self.tensionCondensateur = 0

    def afficher(self):
        print "ROBOT"
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print 'Orientation : %d' % self.orientation
        print "---------------------------------------------------"
