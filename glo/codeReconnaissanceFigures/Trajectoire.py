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
        self.dimensionPixel = (self.resolution[0]*3/16, self.resolution[0]*11/12, 0, self.resolution[1])
        self.dimensionReel = (100, 300)
        self.intervalle = 1
        self.depart = Cellule()
        self.arriver = Cellule()

    def initElement(self, listIles, listTresors):
        self.listIles = listIles
        self.listeTresors = listTresors

    def initListCellules(self):
        atteignableX = True
        atteignableY = True
        for x in range(self.dimensionPixel[2], self.dimensionPixel[3], round((self.dimensionPixel[4]-self.dimensionPixel[3])/self.dimensionReel[1]/self.intervalle)):
            if (not self.xEstAtteignable(x)):
                atteignableX = False
            for y in range (self.dimensionPixel[0], self.dimensionPixel[1], round((self.dimensionPixel[1]-self.dimensionPixel[0])/self.dimensionReel[0]/self.intervalle)):
                if (atteignableX):
                    self.listeCellules.append(Cellule(x, y, True))
                elif (self.yEstAtteignable(x)):
                    self.listeCellules.append(Cellule(x, y, True))
                else:
                    self.listeCellules.append(Cellule(x, y, False))
                atteignableY = True
            atteignableX = True

    def xEstAtteignable(self, x):
        nbPixel = round(7.5*(self.dimensionPixel[3]-self.dimensionPixel[2])/self.dimensionReel[1]/self.intervalle)
        for ile in self.listIles:
            if ((x > (ile.centre_x-nbPixel)) and (x < (ile.centre_x+nbPixel))):
                return False
        return True

    def yEstAtteignable(self, y):
        nbPixel = round(7.5*(self.dimensionPixel[1]-self.dimensionPixel[0])/self.dimensionReel[0]/self.intervalle)
        for ile in self.listIles:
            if ((y > (ile.centre_y-nbPixel)) and (y < (ile.centre_y+nbPixel))):
                return False
        return True

    def getHeuristic(self, cellule):
        return 10 * (abs(cellule.x - self.arriver.x) + abs(cellule.y - self.arriver.y))

    def getCellule(self, x, y):
        return self.listeCellules[x * round((self.dimensionPixel[1]-self.dimensionPixel[0]) * self.dimensionReel[0] * self.intervalle) + y]

    def getCelluleAdjacente(self, cellule):
        listCellules = []
        if cellule.x < self.dimensionPixel[3]:
            listCellules.append(self.get_cell(cellule.x+1, cellule.y))
        if cellule.y > self.dimensionPixel[0]:
            listCellules.append(self.get_cell(cellule.x, cellule.y-1))
        if cellule.x > self.dimensionPixel[2]:
            listCellules.append(self.get_cell(cellule.x-1, cellule.y))
        if cellule.y < self.dimensionPixel[1]:
            listCellules.append(self.get_cell(cellule.x, cellule.y+1))
        if ((cellule.x < self.dimensionPixel[3]) and (cellule.y < self.dimensionPixel[1])):
            listCellules.append(self.get_cell(cellule.x+1, cellule.y+1))
        if ((cellule.x > self.dimensionPixel[2]) and (cellule.y > self.dimensionPixel[0])):
            listCellules.append(self.get_cell(cellule.x-1, cellule.y-1))
        if ((cellule.x < self.dimensionPixel[3]) and (cellule.y > self.dimensionPixel[0])):
            listCellules.append(self.get_cell(cellule.x+1, cellule.y-1))
        if ((cellule.x > self.dimensionPixel[2]) and (cellule.y < self.dimensionPixel[1])):
            listCellules.append(self.get_cell(cellule.x-1, cellule.y+11))
	    return listCellules

    def afficherTrajectoire(self):
        cellule = self.arriver
        print "\n--------------------------------------------------"
        print "\nTrajectoire:"
        print "\n--------------------------------------------------"
        while cellule.parent is not self.depart:
            cellule = cellule.parent
            print  "\ncellule: %d,%d" % (cellule.x, cellule.y)

    def rafraichirCellule(self, adjacent, cellule):
        adjacent.g = cellule.g + 10
        adjacent.h = self.getHeuristic(adjacent)
        adjacent.parent = cellule
        adjacent.f = adjacent.h + adjacent.g

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








