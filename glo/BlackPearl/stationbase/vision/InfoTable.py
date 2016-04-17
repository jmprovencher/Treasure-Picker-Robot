import numpy as np

INTERVALLE_TABLE_1_ROBOT = (np.array([30, 5, 140]), np.array([145, 140, 245]))
INTERVALLE_TABLE_5_ROBOT = (np.array([80, 60, 130]), np.array([140, 120, 210]))
INTERVALLE_TABLE_1_TRESOR = (np.array([0, 53, 50]), np.array([30, 160, 150]))
INTERVALLE_TABLE_2_TRESOR = (np.array([0, 53, 50]), np.array([30, 160, 150]))
INTERVALLE_TABLE_5_TRESOR = (np.array([0, 50, 90]), np.array([60, 140, 140]))
INTERVALLE_TABLE_6_TRESOR = (np.array([0, 50, 80]), np.array([40, 140, 140]))
INTERVALLE_TABLE_1_RECTANGLE = (np.array([20, 100, 10]), np.array([185, 210, 190]))
INTERVALLE_TABLE_2_RECTANGLE = (np.array([20, 100, 10]), np.array([185, 210, 190]))
INTERVALLE_TABLE_5_RECTANGLE = (np.array([20, 100, 10]), np.array([185, 210, 190]))
INTERVALLE_TABLE_6_RECTANGLE  = (np.array([20, 100, 10]), np.array([185, 210, 190]))
INTERVALLE_TABLE_1_ROUGE = (np.array([0, 0, 70]), np.array([70, 50, 200]))
INTERVALLE_TABLE_5_ROUGE = (np.array([15, 0, 75]), np.array([100, 65, 200]))
INTERVALLE_TABLE_1_BLEU = (np.array([102, 102, 0]), np.array([255, 255, 102]))
INTERVALLE_TABLE_5_BLEU = (np.array([120, 120, 0]), np.array([190, 170, 80]))
INTERVALLE_TABLE_1_VERT = (np.array([0, 70, 0]), np.array([100, 200, 80]))
INTERVALLE_TABLE_5_VERT = (np.array([0, 70, 0]), np.array([100, 200, 80]))
INTERVALLE_TABLE_1_JAUNE = (np.array([0, 90, 91]), np.array([50, 194, 210]))
INTERVALLE_TABLE_5_JAUNE = (np.array([0, 50, 50]), np.array([50, 255, 255]))


class InfoTable:
    def __init__(self, type, numeroTable):
        self.setIntervalle(type, numeroTable)
        self.setCrop(numeroTable)
        
    def setIntervalle(self, type, numeroTable):

        if type == 'Robot':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = INTERVALLE_TABLE_1_ROBOT
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = INTERVALLE_TABLE_5_ROBOT

        elif type == 'Tresor':
            if numeroTable == 1:
                self.intervalle = INTERVALLE_TABLE_1_TRESOR
            elif numeroTable == 2 or numeroTable == 3:
                self.intervalle = INTERVALLE_TABLE_2_TRESOR
            elif numeroTable == 5:
                self.intervalle = INTERVALLE_TABLE_5_TRESOR
            elif numeroTable == 6:
                self.intervalle = INTERVALLE_TABLE_6_TRESOR

        elif type == 'Rectangle':
            if numeroTable == 1:
                self.intervalle = INTERVALLE_TABLE_1_RECTANGLE
            elif numeroTable == 2 or numeroTable == 3:
                self.intervalle = INTERVALLE_TABLE_2_RECTANGLE
            elif numeroTable == 5:
                self.intervalle = INTERVALLE_TABLE_5_RECTANGLE
            elif numeroTable == 6:
                self.intervalle = INTERVALLE_TABLE_6_RECTANGLE


        elif type == 'Rouge':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = INTERVALLE_TABLE_1_ROUGE
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = INTERVALLE_TABLE_5_ROUGE
                
        elif type == 'Bleu':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                INTERVALLE_TABLE_1_BLEU
            elif numeroTable == 5 or numeroTable == 6:
                INTERVALLE_TABLE_5_BLEU
                
        elif type == 'Vert':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle = INTERVALLE_TABLE_1_VERT
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = INTERVALLE_TABLE_5_VERT
                
        elif type == 'Jaune':
            if numeroTable == 1 or numeroTable == 2 or numeroTable == 3:
                self.intervalle =  INTERVALLE_TABLE_1_JAUNE
            elif numeroTable == 5 or numeroTable == 6:
                self.intervalle = INTERVALLE_TABLE_5_JAUNE

    def setCrop(self, numeroTable):
        # La difference en y2 et y1 doit etre de 855 pixel
        if numeroTable == 1:
            self.crop = (155, 1010)
        elif numeroTable == 2:
            self.crop = (155, 1010)
        elif numeroTable == 3:
            self.crop = (150, 1005)
        elif numeroTable == 5:
            self.crop = (190, 1045)
        elif numeroTable == 6:
            self.crop = (133, 988)

    def setCorrectionAngle(self, numeroTable):
        # La difference en y2 et y1 doit etre de 855 pixel
        if numeroTable == 1:
            self.crop = (155, 1010)
        elif numeroTable == 2:
            self.crop = (155, 1010)
        elif numeroTable == 3:
            self.crop = (150, 1005)
        elif numeroTable == 5:
            self.crop = (190, 1045)
        elif numeroTable == 6:
            self.crop = (133, 988)

                
    def getIntervalle(self):
        return self.intervalle

    def getCrop(self):
        return self.crop
