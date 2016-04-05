import numpy as np


class InfoTable:
    def __init__(self, type, numeroTable):
        self.setIntervalle(type, numeroTable)
        self.setCrop(numeroTable)
        
    def setIntervalle(self, type, numeroTable):
        if type == 'Robot':
            self.intervalle = (np.array([30, 5, 140]), np.array([145, 140, 245]))
            
        elif type == 'Tresor':
            if self.numeroTable == 1:
                self.intervalle = (np.array([50, 160, 160]), np.array([6, 100, 100]))
            elif self.numeroTable == 2 or self.numeroTable == 3:
                self.intervalle = (np.array([30, 160, 150]), np.array([0, 53, 50]))
            elif self.numeroTable == 5 or self.numeroTable == 6:
                self.intervalle = (np.array([41, 70, 84]), np.array([0 , 53 ,50]))
                
        elif type == 'Rouge':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = (np.array([0, 0, 70]), np.array([70, 50, 200]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([15, 0, 75]), np.array([100, 65, 200]))
                
        elif type == 'Bleu':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = (np.array([102, 102, 0]), np.array([255, 255, 102]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([102, 102, 0]), np.array([255, 255, 102]))
                
        elif type == 'Vert':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = (np.array([0, 0, 70]), np.array([70, 50, 200]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([0, 70, 0]), np.array([100, 200, 80]))
                
        elif type == 'Jaune':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle =  (np.array([0, 90, 91]), np.array([50, 194, 210]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([0, 50, 50]), np.array([50, 255, 255]))

    def setCrop(self, numeroTable):
        if numeroTable == 5:
            self.crop = (190, 1045)
                
    def getIntervalle(self):
        return self.intervalle

    def getCrop(self):
        return self.crop
