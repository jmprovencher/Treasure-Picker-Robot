class AlignementIle():
    def __init__(self):
        self.terminer = False

    def completerDepot(self):
        print("Dropping that BOMB")
        self.terminer = True

    def ajusterPosition(self, distance_x, distance_y):
        self._ajusterPositionX(distance_x)
        self._ajusterPositionY(distance_y)

    def _ajusterPositionX(self, distance_x):
        if (distance_x < 0):
            # Deplacer vers la gauche
            pass
        elif (distance_x > 0):
            # Deplacer vers la droite
            pass
        print("Deplacement x: %d" % distance_x)

    def _ajusterPositionY(self, distance_y):
        if (distance_y < 0):
            # Reculer
            pass
        elif (distance_y > 0):
            # Avancer
            pass
        print("Deplacement y: %d" % distance_y)
