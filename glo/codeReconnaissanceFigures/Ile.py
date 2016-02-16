# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique

class Ile(ElementCartographique):

    def __init__(self,x,y,couleur,forme):
        self.m_x = x
        self.m_y = y
        self.m_couleur = couleur
        self.m_forme = forme

    def getForme(self):
        return self.m_forme

    def getCouleur(self):
        return self.m_couleur

    def afficher(self):
        print "ILE"
        print "%s %s" % (self.m_forme, self.m_couleur)
        print "Position x : %d" % self.m_x
        print "Position y : %d" % self.m_y
        print "---------------------------------------------------"


