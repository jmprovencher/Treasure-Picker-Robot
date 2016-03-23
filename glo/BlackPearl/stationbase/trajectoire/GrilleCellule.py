# import the necessary packages
from __future__ import division
from stationbase.trajectoire.Cellule import Cellule

class GrilleCellule():
    def __init__(self):
        self.listeCellules = []
        self.resolution = (1600, 1200)
        self.dimensionCrop = (1600, 855)
        self.dimensionReel = (300, 100)
        self.incrementX = int((self.dimensionCrop[0]) // self.dimensionReel[0])
        self.incrementY = int((self.dimensionCrop[1]) // self.dimensionReel[1])
        self.rayonBuffer = 15
        self.listeIles = None

    def initGrilleCellule(self, listeIles):
        self.listeCellules = []
        self.listeIles = listeIles
        for x in range(0, self.dimensionCrop[0], self.incrementX):
            for y in range(0, self.dimensionCrop[1], self.incrementY):
                    self.listeCellules.append(Cellule(x, y, self.estAtteignable(x, y, listeIles)))
                
    def depPixelXACentimetre(self, pix):
        return int(round(pix * (self.dimensionReel[0]) // self.dimensionCrop[0]))
    
    def depPixelYACentimetre(self, pix):
        return int(round(pix * (self.dimensionReel[1]) // self.dimensionCrop[1]))

    def depCentimetreYAPixel(self, cent):
        return int(round(cent * (self.dimensionCrop[1]) // self.dimensionReel[1]))
    
    def distanceAIleAuCarre(self, x, y, ile):
        distanceX = ile.centre_x - x
        distanceY = ile.centre_y - y
        distanceX = self.depPixelXACentimetre(distanceX)
        distanceY = self.depPixelYACentimetre(distanceY)
        distanceCarre = distanceX**2 + distanceY**2
        return distanceCarre
                
    def estAtteignable(self, x, y, listeIles):
        if (y <= self.depCentimetreYAPixel(self.rayonBuffer)) or (y >= self.dimensionCrop[1]-self.depCentimetreYAPixel(self.rayonBuffer)):
            return False
        elif not self.listeIles is None:
            for ile in listeIles:
                if  (self.distanceAIleAuCarre(x, y, ile) <= self.rayonBuffer**2):
                    return False
        return True

    def getCellule(self, x, y):
        return self.listeCellules[
            ((x // self.incrementX)) * ((self.dimensionCrop[1] // self.incrementY + 1)) + ((y // self.incrementY))]

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
