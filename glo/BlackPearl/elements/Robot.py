from elements.ElementCartographique import ElementCartographique


class Robot(ElementCartographique):
    def __init__(self, centre, orientation):
        ElementCartographique.__init__(self, centre)
        self.orientation = orientation

    def getOrientation(self):
        return self.orientation
