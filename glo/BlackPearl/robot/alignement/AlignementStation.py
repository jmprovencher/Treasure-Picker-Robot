class AlignementStation():
    def __init__(self):
        self.terminer = False
        self.ajustements = []

    def calculerAjustement(self, distance_x, distance_y):
        ajustements_x = self._ajusterPositionX(distance_x)
        ajustements_y = self._ajusterPositionY(distance_y)
        self.ajustements.append(ajustements_x)
        self.ajustements.append(ajustements_y)
        return self.ajustements


    def _ajusterPositionX(self, distance_x):
        if (distance_x < 0):
            commande = 'left'
        elif (distance_x > 0):
            commande = 'right'

        return commande, distance_x

    def _ajusterPositionY(self, distance_y):
        if (distance_y < 0):
            commande = 'backward'
        elif (distance_y > 0):
            commande = 'forward'

        return commande, distance_y