# import the necessary packages
import heapq

from Cellule import Cellule


class AlgoAEtoile():

    def __init__(self, grilleCellule):
        self.grilleCellule = grilleCellule
        self.ouvert = []
        heapq.heapify(self.ouvert)
        self.fermer = set()
        self.trajet = []
        self.depart = None
        self.arriver = None
        
    def trouverTrajet(self, depart, arriver):
        self.setDepart(depart)
        self.setArriver(arriver)
        heapq.heappush(self.ouvert, (self.depart.f, self.depart))
        while len(self.ouvert):
            f, cellule = heapq.heappop(self.ouvert)
            self.fermer.add(cellule)
            if self.estArriver(cellule):
                #self.afficherTrajectoireDetailler()
                self.simplifierTrajectoire()
                return self.trajet
                break
            adjacents = self.grilleCellule.getCelluleAdjacente(cellule)
            for adj in adjacents:
                if adj.atteignable and adj not in self.fermer:
                    if (adj.f, adj) in self.ouvert:
                        if adj.g > cellule.g + 10:
                            self.rafraichirCellule(adj, cellule)
                    else:
                        self.rafraichirCellule(adj, cellule)
                        heapq.heappush(self.ouvert, (adj.f, adj))
        self.trajet = []
        return self.trajet
        
    def simplifierTrajectoire(self):
        self.trajet = [(self.arriver.x, self.arriver.y)]
        cellule = self.grilleCellule.getCellule(self.arriver.x, self.arriver.y)
        depX = cellule.x - cellule.parent.x
        depY = cellule.y - cellule.parent.y
        while not self.estDepart(cellule.parent):
            tmp = cellule
            cellule = cellule.parent
            if not ((tmp.x - cellule.x == depX) and (tmp.y - cellule.y == depY)):
                self.trajet.append((tmp.x, tmp.y))
                depX = tmp.x - cellule.x
                depY = tmp.y - cellule.y
        tmp = cellule
        cellule = cellule.parent
        if not ((tmp.x - cellule.x == depX) and (tmp.y - cellule.y == depY)):
            self.trajet.append((tmp.x, tmp.y))
            depX = tmp.x - cellule.x
            depY = tmp.y - cellule.y
        self.trajet.append((self.depart.x, self.depart.y))

    def afficherTrajectoireDetailler(self):
        cellule = self.grilleCellule.getCellule(self.arriver.x, self.arriver.y)
        print "\n******************************************************************************"
        print "Trajectoire:"
        print "******************************************************************************\n"
        print "Arriver: cellule: %d, %d\n" % (self.arriver.x, self.arriver.y)
        if (self.trajet == []):
            print "Aucun trajet!"
        else:
            while not self.estDepart(cellule.parent):
                if (cellule.parent == None):
                    print "Aucun trajet!"
                else:
                    cellule = cellule.parent
                    print  "cellule: %d, %d" % (cellule.x, cellule.y)
        print "\nDepart: cellule: %d, %d" % (self.depart.x, self.depart.y)

    def rafraichirCellule(self, adjacent, cellule):
        adjacent.g = cellule.g + 10
        adjacent.h = adjacent.getHeuristic(self.arriver)
        adjacent.parent = cellule
        adjacent.f = adjacent.h + adjacent.g                        

    def setDepart(self, depart):
        x, y = depart
        while (not (x%self.grilleCellule.incX == 0)):
            x = x + 1
        while (not (y%self.grilleCellule.incY == 0)):
            y = y + 1
        self.depart = Cellule(x, y, True)

    def setArriver(self, arriver):
        x, y = arriver
        while (not (x%self.grilleCellule.incX == 0)):
            x = x + 1
        while (not (y%self.grilleCellule.incY == 0)):
            y = y + 1
        self.arriver = Cellule(x, y, True)

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














