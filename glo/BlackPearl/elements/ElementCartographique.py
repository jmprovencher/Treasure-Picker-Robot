class ElementCartographique():
    def __init__(self, centre):
        self.centre_x, self.centre_y = centre

    def getX(self):
        return self.centre_x

    def getY(self):
        return self.centre_y
