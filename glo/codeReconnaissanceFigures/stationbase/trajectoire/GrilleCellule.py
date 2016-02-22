# import the necessary packages
from Cellule import Cellule

class GrilleCellule():

    def __init__(self):
        self.listeCellules = []
        self.resolution = (1600, 1200)
        self.dimensionCrop = (1600, 850)
        self.dimensionReel = (300, 100)
        self.incX = int((self.dimensionCrop[0])/self.dimensionReel[0])
        self.incY = int((self.dimensionCrop[1])/self.dimensionReel[1])
        self.bufferIle = 20

    def initGrilleCellule(self, listeIles):
        self.listeCellules = []
        atteignableX = True
        for x in range(0, self.dimensionCrop[0], self.incX):
            if (not self.xEstAtteignable(x, listeIles)):
                atteignableX = False
            for y in range (0, self.dimensionCrop[1], self.incY):
                if (atteignableX):
                    self.listeCellules.append(Cellule(x, y, True))
                elif (self.yEstAtteignable(y, listeIles)):
                    self.listeCellules.append(Cellule(x, y, True))
                else:
                    self.listeCellules.append(Cellule(x, y, False))
            atteignableX = True

    def xEstAtteignable(self, x, listeIles):
        nbPixel = int(round(self.bufferIle*(self.dimensionCrop[0])/self.dimensionReel[0]))
        for ile in listeIles:
            if ((x > (ile.centre_x-nbPixel)) and (x < (ile.centre_x+nbPixel))):
                return False
        return True

    def yEstAtteignable(self, y, listeIles):
        nbPixel = int(round(self.bufferIle*(self.dimensionCrop[1])/self.dimensionReel[1]))
        for ile in listeIles:
            if ((y > (ile.centre_y-nbPixel)) and (y < (ile.centre_y+nbPixel))):
                return False
        return True

    def getCellule(self, x, y):
        return self.listeCellules[((x/self.incX)) * ((self.dimensionCrop[1]/self.incY+1)) + ((y/self.incY))]

    def getCelluleAdjacente(self, cellule):
        listCellules = []
        if cellule.x < self.dimensionCrop[0]-self.incX:
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y))
        if cellule.y >= 0+self.incY:
            listCellules.append(self.getCellule(cellule.x, cellule.y-self.incY))
        if cellule.x >= 0+self.incX:
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y))
        if cellule.y < self.dimensionCrop[1]-self.incY:
            listCellules.append(self.getCellule(cellule.x, cellule.y+self.incY))
        if ((cellule.x < self.dimensionCrop[0]-self.incX) and (cellule.y < self.dimensionCrop[1]-self.incY)):
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y+self.incY))
        if ((cellule.x >= 0+self.incX) and (cellule.y >= 0+self.incY)):
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y-self.incY))
        if ((cellule.x < self.dimensionCrop[0]-self.incX) and (cellule.y >= 0+self.incY)):
            listCellules.append(self.getCellule(cellule.x+self.incX, cellule.y-self.incY))
        if ((cellule.x >= 0+self.incX) and (cellule.y < self.dimensionCrop[1]-self.incY)):
            listCellules.append(self.getCellule(cellule.x-self.incX, cellule.y+self.incY))
        return listCellules


















