# import the necessary packages
import numpy as np


class Cellule():

    def __init__(self, *args):
        if (len(args) == 0):
            self.atteignable = True
            self.x = 0
            self.y = 0
            self.parent = None
            self.g = 0
            self.h = 0
            self.f = 0
        else:
            self.atteignable = args[2]
            self.x = args[0]
            self.y = args[1]
            self.parent = None
            self.g = 0
            self.h = 0
            self.f = 0