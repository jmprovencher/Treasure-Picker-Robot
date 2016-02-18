# import the necessary packages
import numpy as np
import heapq
from ElementCartographique import ElementCartographique
from Ile import Ile
from Tresor import Tresor
from Cellule import Cellule

class Trajectoire():

    def __init__(self):
        self.listeIles = []
        self.listeTresors = []
        self.listeCellules = []
        self.ouvert = []
        heapq.heapify(self.ouvert)
        self.fermer = set()
        self.resolution = (480, 640)
        self.dimensionCrop = ((self.resolution[0]*11/12)-(self.resolution[0]*3/16), self.resolution[1])
        self.dimensionReel = (100, 300)
        self.intervalle = 1
        self.depart = Cellule()
        self.arriver = Cellule()
        self.incX = int(round((self.dimensionCrop[1])/self.dimensionReel[1]/self.intervalle))
        self.incY = int(round((self.dimensionCrop[0])/self.dimensionReel[0]/self.intervalle))

    def initElement(self, listeIles, listTresors):
        self.listeIles = listeIles
        self.listeTresors = listTresors

    def initListCellules(self):
        if (len(self.listeCellules) == 0):
            atteignableX = True
            atteignableY = True
            for x in range(0, self.dimensionCrop[1], self.incX):
                if (not self.xEstAtteignable(x)):
                    atteignableX = False
                for y in range (0, self.dimensionCrop[0], self.incY):
                    if (atteignableX):
                        self.listeCellules.append(Cellule(x, y, True))
                    elif (self.yEstAtteignable(x)):
                        self.listeCellules.append(Cellule(x, y, True))
                    else:
                        self.listeCellules.append(Cellule(x, y, False))
                    atteignableY = True
                atteignableX = True

    def xEstAtteignable(self, x):
        nbPixel = int(round(7.5*(self.dimensionCrop[1])/self.dimensionReel[1]/self.intervalle))
        for ile in self.listeIles:
            if ((x > (ile.centre_x-nbPixel)) and (x < (ile.centre_x+nbPixel))):
                return False
        return True

    def yEstAtteignable(self, y):
        nbPixel = int(round(7.5*(self.dimensionCrop[1]-self.dimensionCrop[0])/self.dimensionReel[0]/self.intervalle))
        for ile in self.listeIles:
            if ((y > (ile.centre_y-nbPixel)) and (y < (ile.centre_y+nbPixel))):
                return False
        return True

    def getHeuristic(self, cellule):
        return 10 * (abs(cellule.x - self.arriver.x) + abs(cellule.y - self.arriver.y))

    def getCellule(self, x, y):
        return self.listeCellules[(x/self.incX) * (self.dimensionCrop[0]/self.incY) + (y/self.incY)]

    def getCelluleAdjacente(self, cellule):
        listCellules = []
        if cellule.x < self.dimensionCrop[1]:
            c = self.getCellule(cellule.x+self.incX, cellule.y)
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y))
        if cellule.y > 0:
            listCellules.append(self.getCellule(cellule.x, cellule.y-self.incY))
        if cellule.x > 0:
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y))
        if cellule.y < self.dimensionCrop[0]:
            listCellules.append(self.getCellule(cellule.x, cellule.y+self.incY))
        if ((cellule.x < self.dimensionCrop[1]) and (cellule.y < self.dimensionCrop[0])):
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y+self.incY))
        if ((cellule.x > 0) and (cellule.y > 0)):
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y-self.incY))
        if ((cellule.x < self.dimensionCrop[1]) and (cellule.y > 0)):
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y-self.incY))
        if ((cellule.x > 0) and (cellule.y < self.dimensionCrop[0])):
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y+self.incY))
	    return listCellules

    def afficherTrajectoire(self):
        cellule = self.arriver
        print "\n******************************************************************************"
        print "Trajectoire:"
        print "******************************************************************************\n"
        while cellule.parent is not self.depart:
            cellule = cellule.parent
            print  "\ncellule: %d,%d" % (cellule.x, cellule.y)

    def rafraichirCellule(self, adjacent, cellule):
        adjacent.g = cellule.g + 10
        adjacent.h = self.getHeuristic(adjacent)
        adjacent.parent = cellule
        adjacent.f = adjacent.h + adjacent.g

    def setDepart(self, x, y):
        while (not (x%self.incX == 0)):
            x = x + 1
        while (not (y%self.incY == 0)):
            y = y + 1
        self.depart = Cellule(x, y, True)

    def setArriver(self, x, y):
        while (not (x%self.incX == 0)):
            x = x + 1
        while (not (y%self.incY == 0)):
            y = y + 1
        self.arriver = Cellule(x, y, True)

    def trouverTrajet(self):
        heapq.heappush(self.ouvert, (self.depart.f, self.depart))
        while len(self.ouvert):
            f, cellule = heapq.heappop(self.ouvert)
            self.fermer.add(cellule)
            if cellule is self.arriver:
                self.afficherTrajectoire()
                break
            adjacents = self.getCelluleAdjacente(cellule)
            for adj in adjacents:
                if adj.atteignable and adj not in self.fermer:
                    if (adj.f, adj) in self.ouvert:
                        if adj.g > cellule.g + 10:
                            self.rafraichirCellule(adj, cellule)
                        else:
                            self.rafraichirCellule(adj, cellule)
                            heapq.heappush(self.ouvert, (adj.f, adj))









