# import the necessary packages
from stationbase.trajectoire.Cellule import Cellule


class GrilleCellule():
    def __init__(self):
        self.listeCellules = []
        self.resolution = (1600, 1200)
        self.dimensionCrop = (1600, 850)
        self.dimensionReel = (300, 100)
        self.incrementX = int((self.dimensionCrop[0]) / self.dimensionReel[0])
        self.incrementY = int((self.dimensionCrop[1]) / self.dimensionReel[1])
        self.bufferIle = 20

    def initGrilleCellule(self, listeIles):
        self.listeCellules = []
        atteignable_x = True

        for x in range(0, self.dimensionCrop[0], self.incrementX):
            if (not self.xEstAtteignable(x, listeIles)):
                atteignable_x = False
            for y in range(0, self.dimensionCrop[1], self.incrementY):
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
            ((x / self.incrementX)) * ((self.dimensionCrop[1] / self.incrementY + 1)) + ((y / self.incrementY))]

    def getCelluleAdjacentes(self, cellule):
        listCellules = []

        if cellule.x < self.dimensionCrop[0] - self.incrementX:
            listCellules.append(self.getCellule(cellule.x + self.incrementX, cellule.y))

        if cellule.y >= 0 + self.incrementY:
            listCellules.append(self.getCellule(cellule.x, cellule.y - self.incrementY))

        if cellule.x >= 0 + self.incrementX:
            listCellules.append(self.getCellule(cellule.x - self.incrementX, cellule.y))

        if cellule.y < self.dimensionCrop[1] - self.incrementY:
            listCellules.append(self.getCellule(cellule.x, cellule.y + self.incrementY))

        if ((cellule.x < self.dimensionCrop[0] - self.incrementX) and (
                    cellule.y < self.dimensionCrop[1] - self.incrementY)):
            listCellules.append(self.getCellule(cellule.x + self.incrementX, cellule.y + self.incrementY))

        if ((cellule.x >= 0 + self.incrementX) and (cellule.y >= 0 + self.incrementY)):
            listCellules.append(self.getCellule(cellule.x - self.incrementX, cellule.y - self.incrementY))

        if ((cellule.x < self.dimensionCrop[0] - self.incrementX) and (cellule.y >= 0 + self.incrementY)):
            listCellules.append(self.getCellule(cellule.x + self.incrementX, cellule.y - self.incrementY))

        if ((cellule.x >= 0 + self.incrementX) and (cellule.y < self.dimensionCrop[1] - self.incrementY)):
            listCellules.append(self.getCellule(cellule.x - self.incrementX, cellule.y + self.incrementY))

        return listCellules
