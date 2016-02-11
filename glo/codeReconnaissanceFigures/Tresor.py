# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique

class Tresor(ElementCartographique):

    def __init__(self,x,y):
        self.m_x = x
        self.m_y = y

    def afficher(self):
        print "TRESOR"
        print "Position x : %d",self.m_x
        print "Position y : %d",self.m_y

