# import the necessary packages
import numpy as np


class Cellule():

    def __init__(self):
        self.atteignable = True
        self.x = 0
        self.y = 0
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __init__(self, x, y, atteignable):
        self.atteignable = atteignable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
