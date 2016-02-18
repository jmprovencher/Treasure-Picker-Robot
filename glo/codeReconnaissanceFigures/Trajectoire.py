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
        self.resolution = (1200, 1600)
        self.dimensionCrop = ((self.resolution[0]*11/12)-(self.resolution[0]*3/16), self.resolution[1])
        self.dimensionReel = (100, 300)
        self.intervalle = 1
        self.depart = Cellule()
        self.arriver = Cellule()
        self.incX = int((self.dimensionCrop[1])/self.dimensionReel[1]/self.intervalle)
        self.incY = int((self.dimensionCrop[0])/self.dimensionReel[0]/self.intervalle)
        self.trajetSimplifier = []

    def initElement(self, listeIles, listTresors):
        self.listeIles = listeIles
        self.listeTresors = listTresors

    def initListCellules(self):
        if (len(self.listeCellules) == 0):
            atteignableX = True
            for x in range(0, self.dimensionCrop[1], self.incX):
                if (not self.xEstAtteignable(x)):
                    atteignableX = False
                for y in range (0, self.dimensionCrop[0], self.incY):
                    if (atteignableX):
                        self.listeCellules.append(Cellule(x, y, True))
                    elif (self.yEstAtteignable(y)):
                        self.listeCellules.append(Cellule(x, y, True))
                    else:
                        self.listeCellules.append(Cellule(x, y, False))
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
        return self.listeCellules[((x/self.incX)) * ((self.dimensionCrop[0]/self.incY)+1) + ((y/self.incY))]

    def getCelluleAdjacente(self, cellule):
        listCellules = []
        if cellule.x < self.dimensionCrop[1]-self.incX:
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y))
        if cellule.y >= 0+self.incY:
            listCellules.append(self.getCellule(cellule.x, cellule.y-self.incY))
        if cellule.x >= 0+self.incX:
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y))
        if cellule.y < self.dimensionCrop[0]-self.incY:
            listCellules.append(self.getCellule(cellule.x, cellule.y+self.incY))
        if ((cellule.x < self.dimensionCrop[1]-self.incX) and (cellule.y < self.dimensionCrop[0]-self.incY)):
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y+self.incY))
        if ((cellule.x >= 0+self.incX) and (cellule.y >= 0+self.incY)):
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y-self.incY))
        if ((cellule.x < self.dimensionCrop[1]-self.incX) and (cellule.y >= 0+self.incY)):
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y-self.incY))
        if ((cellule.x >= 0+self.incX) and (cellule.y < self.dimensionCrop[0]-self.incY)):
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y+self.incY))
        return listCellules

    def afficherTrajectoire(self):
        cellule = self.getCellule(self.arriver.x, self.arriver.y)
        print "\n******************************************************************************"
        print "Trajectoire:"
        print "******************************************************************************\n"
        print "Arriver: cellule: %d, %d\n" % (self.arriver.x, self.arriver.y)
        while not self.estDepart(cellule.parent):
            cellule = cellule.parent
            print  "cellule: %d, %d" % (cellule.x, cellule.y)
        print "\nDepart: cellule: %d, %d" % (self.depart.x, self.depart.y)

    def afficherTrajectoireSimplifier(self):
        cellule = self.getCellule(self.arriver.x, self.arriver.y)
        print "\n******************************************************************************"
        print "Trajectoire simplifier:"
        print "******************************************************************************\n"
        print "Arriver: cellule: %d, %d\n" % (self.arriver.x, self.arriver.y)
        for dep in range(len(self.trajetSimplifier)):
            print "cellule: %d, %d" % self.trajetSimplifier[dep]
        print "\nDepart: cellule: %d, %d" % (self.depart.x, self.depart.y)

    def simplifierTrajectoire(self):
        self.trajetSimplifier = []
        cellule = self.getCellule(self.arriver.x, self.arriver.y)
        depX = cellule.x - cellule.parent.x
        depY = cellule.y - cellule.parent.y
        while not self.estDepart(cellule.parent):
            tmp = cellule
            cellule = cellule.parent
            if not ((tmp.x - cellule.x == depX) and (tmp.y - cellule.y == depY)):
                self.trajetSimplifier.append((tmp.x, tmp.y))
                depX = tmp.x - cellule.x
                depY = tmp.y - cellule.y
        tmp = cellule
        cellule = cellule.parent
        if not ((tmp.x - cellule.x == depX) and (tmp.y - cellule.y == depY)):
            self.trajetSimplifier.append((tmp.x, tmp.y))
            depX = tmp.x - cellule.x
            depY = tmp.y - cellule.y

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
            if self.estArriver(cellule):
                break
            # print "%d, %d" % (cellule.x, cellule.y)
            adjacents = self.getCelluleAdjacente(cellule)
            for adj in adjacents:
                if adj.atteignable and adj not in self.fermer:
                    if (adj.f, adj) in self.ouvert:
                        if adj.g > cellule.g + 10:
                            self.rafraichirCellule(adj, cellule)
                    else:
                        self.rafraichirCellule(adj, cellule)
                        heapq.heappush(self.ouvert, (adj.f, adj))

    def estArriver(self, cellule):
        if (cellule.x == self.arriver.x) and (cellule.y == self.arriver.y):
            return True
        else:
            return False

    def estDepart(self, cellule):
        if (cellule.x == self.depart.x) and (cellule.y == self.depart.y):
            return True
        else:
            return False













