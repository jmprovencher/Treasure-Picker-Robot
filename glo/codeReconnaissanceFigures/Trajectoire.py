# import the necessary packages
import numpy as np
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor

class Trajectoire():

    def __init__(self):
        self.listeIles = []
        self.listeTresors = []
        self.matricePosition = []
        self.resolution = (480, 640)

    def initElement(self, listIles, listTresors):
        self.listIles = listIles
        self.listeTresors = listTresors

    #def initMatrice(self):


