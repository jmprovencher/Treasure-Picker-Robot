# import the necessary packages
import heapq

from stationbase.trajectoire.Cellule import Cellule

class AlgorithmeTrajectoire():
    def __init__(self, grilleCellule):
        self.grilleCellule = grilleCellule
        self.heapOuvert = []
        heapq.heapify(self.heapOuvert)
        self.trajet = []
        self.fermer = set()
        self.depart = None
        self.arriver = None

    def trouverTrajet(self, depart, arriver):
        self.setDepart(depart)
        self.setArriver(arriver)
        heapq.heappush(self.heapOuvert, (self.depart.priorite, self.depart))

        while len(self.heapOuvert):
            f, cellule = heapq.heappop(self.heapOuvert)
            self.fermer.add(cellule)
            if self.estArriver(cellule):
                self.simplifierTrajet()
                return self.trajet
                break

            cellulesAdjacentes = self.grilleCellule.getCelluleAdjacentes(cellule)
            for adj in cellulesAdjacentes:
                if adj.atteignable and adj not in self.fermer:
                    if (adj.priorite, adj) in self.heapOuvert:
                        if adj.poid > cellule.poid + 10:
                            self.rafraichirCellule(adj, cellule)
                    else:
                        self.rafraichirCellule(adj, cellule)
                        heapq.heappush(self.heapOuvert, (adj.priorite, adj))

        self.trajet = []
        return self.trajet

    def simplifierTrajet(self):
        self.trajet = [(self.arriver.x, self.arriver.y)]
        cellule = self.grilleCellule.getCellule(self.arriver.x, self.arriver.y)
        depart_x = cellule.x - cellule.parent.x
        depart_y = cellule.y - cellule.parent.y

        while not self.estDepart(cellule.parent):
            temp = cellule
            cellule = cellule.parent
            if not ((temp.x - cellule.x == depart_x) and (temp.y - cellule.y == depart_y)):
                self.trajet.append((temp.x, temp.y))
                depart_x = temp.x - cellule.x
                depart_y = temp.y - cellule.y

        temp = cellule
        cellule = cellule.parent

        if not ((temp.x - cellule.x == depart_x) and (temp.y - cellule.y == depart_y)):
            self.trajet.append((temp.x, temp.y))
            depart_x = temp.x - cellule.x
            depart_y = temp.y - cellule.y

        self.trajet.append((depart_x, depart_y))

    def afficherTrajectoireDetailler(self):
        cellule = self.grilleCellule.getCellule(self.arriver.x, self.arriver.y)
        print "\n**************************"
        print "Trajectoire:"
        print "****************************\n"
        print "Arriver: cellule: %d, %d\n" % (self.arriver.x, self.arriver.y)
        if (self.trajet == []):
            print "Aucun trajet!"
        else:
            while not self.estDepart(cellule.parent):
                if (cellule.parent == None):
                    print "Aucun trajet!"
                else:
                    cellule = cellule.parent
                    print "cellule: %d, %d" % (cellule.x, cellule.y)
        print "\nDepart: cellule: %d, %d" % (self.depart.x, self.depart.y)

    def rafraichirCellule(self, celluleAdjacente, cellule):
        celluleAdjacente.poid = cellule.poid + 10
        celluleAdjacente.heuristique = celluleAdjacente.getHeuristique(self.arriver)
        celluleAdjacente.parent = cellule
        celluleAdjacente.priorite = celluleAdjacente.heuristique + celluleAdjacente.poid

    def setDepart(self, depart):
        depart_x, depart_y = depart
        while not (depart_x % self.grilleCellule.incrementX == 0):
            depart_x += 1
        while not (depart_y % self.grilleCellule.incrementY == 0):
            depart_y += 1
        self.depart = Cellule(depart_x, depart_y, True)

    def setArriver(self, arriver):
        arriver_x, arriver_y = arriver
        while not (arriver_x % self.grilleCellule.incrementX == 0):
            arriver_x += 1

        while not (arriver_y % self.grilleCellule.incrementY == 0):
            arriver_y += 1
        self.arriver = Cellule(arriver_x, arriver_y, True)

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
