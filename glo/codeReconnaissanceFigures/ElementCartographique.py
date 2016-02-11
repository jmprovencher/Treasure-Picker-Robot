# import the necessary packages
import numpy as np

class ElementCartographique():

    def __init__(self,x,y):
        self.m_x = x
        self.m_y = y

    def getX(self):
        return self.m_x

    def getY(self):
        return self.m_y

