# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique

class Ile(ElementCartographique):

    def __init__(self,x,y,couleur,forme):
        m_x = x
        m_y = y
        m_couleur = couleur
        m_forme = forme

    def getForme(self):
        return self.m_forme

    def getCouleur(self):
        return self.m_couleur


