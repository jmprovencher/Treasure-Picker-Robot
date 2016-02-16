# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique

class Tresor(ElementCartographique):

    def __init__(self, centre):
        self.centre_x, self.centre_y = centre

    def afficher(self):
        print "TRESOR"
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print "---------------------------------------------------"

