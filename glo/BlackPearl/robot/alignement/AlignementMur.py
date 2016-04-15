import math

MAX_ORIENTATION = 10
MIN_ORIENTATION = 1

class AlignementMur():
    def __init__(self):
        self.ajustements = []

    def calculerAjustementRotation(self, orientation):
        if (abs(orientation) < MIN_ORIENTATION) or (abs(orientation) > MAX_ORIENTATION):
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