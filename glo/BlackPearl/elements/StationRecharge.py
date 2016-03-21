from elements.ElementCartographique import ElementCartographique

class StationRecharge(ElementCartographique):
    def __init__(self):
        self.centre_x = 1500
        self.centre_y = 5
        self.forme = "Station"

    def afficher(self):
        print "Station"
        print "Position x : %d" % self.centre_x
        print "Position y : %d" % self.centre_y
        print "---------------------------------------------------"
