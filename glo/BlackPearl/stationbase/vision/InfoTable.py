import numpy as np


class InfoTable:
    def __init__(self, type, numeroTable):
        self.setIntervalle(type, numeroTable)
        self.setCrop(numeroTable)
        
    def setIntervalle(self, type, numeroTable):
        if type == 'Robot':
            #seulement no 5 est teste pour l'instant
            if numeroTable == 1:
                self.intervalle = (np.array([80, 60, 130]), np.array([140, 120, 210]))
            else:
                self.intervalle = (np.array([30, 5, 140]), np.array([145, 140, 245]))
            if numeroTable == 2:
                self.intervalle = (np.array([80, 60, 130]), np.array([140, 120, 210]))
            else:
                self.intervalle = (np.array([30, 5, 140]), np.array([145, 140, 245]))
            if numeroTable == 3:
                self.intervalle = (np.array([80, 60, 130]), np.array([140, 120, 210]))
            else:
                self.intervalle = (np.array([30, 5, 140]), np.array([145, 140, 245]))
            if numeroTable == 5:
                self.intervalle = (np.array([80, 60, 130]), np.array([140, 120, 210]))
            else:
                self.intervalle = (np.array([30, 5, 140]), np.array([145, 140, 245]))
            if numeroTable == 6:
                self.intervalle = (np.array([80, 60, 130]), np.array([140, 120, 210]))
            else:
                self.intervalle = (np.array([30, 5, 140]), np.array([145, 140, 245]))

        elif type == 'Tresor':
            if numeroTable == 1:
                self.intervalle = (np.array([50, 160, 160]), np.array([6, 100, 100]))
            elif numeroTable == 2 or numeroTable == 3:
                self.intervalle = (np.array([30, 160, 150]), np.array([0, 53, 50]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([0, 50, 90]), np.array([60, 140, 140]))
                
        elif type == 'Rouge':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = (np.array([0, 0, 70]), np.array([70, 50, 200]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([15, 0, 75]), np.array([100, 65, 200]))
                
        elif type == 'Bleu':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = (np.array([102, 102, 0]), np.array([255, 255, 102]))
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = (np.array([150, 150, 40]), np.array([190, 170, 80]))
                
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
        # La difference en y2 et y1 doit etre de 855 pixel
        #seulement no 5 est teste pour l'instant
        if numeroTable == 1:
            self.crop = (190, 1045)
        if numeroTable == 2:
            self.crop = (190, 1045)
        if numeroTable == 3:
            self.crop = (190, 1045)
        if numeroTable == 5:
            self.crop = (190, 1045)
        if numeroTable == 6:
            self.crop = (190, 1045)

                
    def getIntervalle(self):
        return self.intervalle

    def getCrop(self):
        return self.crop
