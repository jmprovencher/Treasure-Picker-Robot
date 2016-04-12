import math

class AlignementMur():
    def __init__(self):
        self.ajustements = []

    def calculerAjustementRotation(self, orientation):
        if (abs(orientation) < 1) or (abs(orientation) > 10):
            return None
        else:
            ajustement_orientation = self.ajusterOrientation(orientation)
            return ajustement_orientation

    def ajusterOrientation(self, orientation):
        if (orientation < 0):
            commande = 'rotateAntiClockwise'
            degree = abs(orientation)
            parametre = math.floor(degree)
        elif (orientation > 0):
            commande = 'rotateClockwise'
            degree = math.floor(orientation)
            parametre = degree

        return commande, parametre