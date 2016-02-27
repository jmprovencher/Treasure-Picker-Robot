# import the necessary packages
from stationbase.trajectoire.Cellule import Cellule

##### REFACTORING STATUS #####
# 80 % DONE
# PEUT ETRE SIMPLIFIER CONDITIONS DE GETCELLULESADJACENTES AVEC NOUVELLES FONCTIONS DE COMPARAISON

class GrilleCellule():
    def __init__(self):
        self.listeCellules = []
        self.resolution = (1600, 1200)
        self.dimensionCrop = (1600, 850)
        self.dimensionReel = (300, 100)
        self.increment_x = int((self.dimensionCrop[0]) / self.dimensionReel[0])
        self.increment_y = int((self.dimensionCrop[1]) / self.dimensionReel[1])
        self.bufferIle = 20

    def initGrilleCellule(self, listeIles):
        self.listeCellules = []
        atteignable_x = True

        for x in range(0, self.dimensionCrop[0], self.increment_x):
            if (not self.xEstAtteignable(x, listeIles)):
                atteignable_x = False
            for y in range(0, self.dimensionCrop[1], self.increment_y):
                if (atteignable_x):
                    self.listeCellules.append(Cellule(x, y, True))
                elif (self.yEstAtteignable(y, listeIles)):
                    self.listeCellules.append(Cellule(x, y, True))
                else:
                    self.listeCellules.append(Cellule(x, y, False))
            atteignable_x = True

    def xEstAtteignable(self, x, listeIles):
        nombrePixel = int(round(self.bufferIle * (self.dimensionCrop[0]) / self.dimensionReel[0]))

        for ile in listeIles:
            if ((x > (ile.centre_x - nombrePixel)) and (x < (ile.centre_x + nombrePixel))):
                return False
        return True

    def yEstAtteignable(self, y, listeIles):
        nombrePixel = int(round(self.bufferIle * (self.dimensionCrop[1]) / self.dimensionReel[1]))

        for ile in listeIles:
            if ((y > (ile.centre_y - nombrePixel)) and (y < (ile.centre_y + nombrePixel))):
                return False
        return True

    def getCellule(self, x, y):
        return self.listeCellules[
            ((x / self.increment_x)) * ((self.dimensionCrop[1] / self.increment_y + 1)) + ((y / self.increment_y))]

    def getCelluleAdjacente(self, cellule):
        listCellules = []

        if cellule.x < self.dimensionCrop[0] - self.increment_x:
            listCellules.append(self.getCellule(cellule.x + self.increment_x, cellule.y))

        if cellule.y >= 0 + self.increment_y:
            listCellules.append(self.getCellule(cellule.x, cellule.y - self.increment_y))

        if cellule.x >= 0 + self.increment_x:
            listCellules.append(self.getCellule(cellule.x - self.increment_x, cellule.y))

        if cellule.y < self.dimensionCrop[1] - self.increment_y:
            listCellules.append(self.getCellule(cellule.x, cellule.y + self.increment_y))

        if ((cellule.x < self.dimensionCrop[0] - self.increment_x) and (
                    cellule.y < self.dimensionCrop[1] - self.increment_y)):
            listCellules.append(self.getCellule(cellule.x + self.increment_x, cellule.y + self.increment_y))

        if ((cellule.x >= 0 + self.increment_x) and (cellule.y >= 0 + self.increment_y)):
            listCellules.append(self.getCellule(cellule.x - self.increment_x, cellule.y - self.increment_y))

        if ((cellule.x < self.dimensionCrop[0] - self.increment_x) and (cellule.y >= 0 + self.increment_y)):
            listCellules.append(self.getCellule(cellule.x + self.increment_x, cellule.y - self.increment_y))

        if ((cellule.x >= 0 + self.increment_x) and (cellule.y < self.dimensionCrop[1] - self.increment_y)):
            listCellules.append(self.getCellule(cellule.x - self.increment_x, cellule.y + self.increment_y))

        return listCellules
