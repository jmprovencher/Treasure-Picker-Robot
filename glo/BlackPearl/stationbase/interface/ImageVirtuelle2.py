import ConfigPath
import cv2


class ImageVirtuelle2():
    def __init__(self):
        self.imageVirtuelle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/res++/test_image20.png'))
        self.imageVirtuelle = self.imageVirtuelle[155:1010, 0:1600]
        self.police = cv2.FONT_HERSHEY_SIMPLEX

    def dessinerTrajetPrevu(self, debut, fin, trajet):
        self.dessinerDebutFinTrajetPrevu(debut, fin)
        pointInitial = None
        if (len(trajet) == 0):
            cv2.putText(self.imageVirtuelle, 'Aucun trajet disponible', (1000, 800), self.police, 1.5,
                        (0, 0, 255), 2, cv2.LINE_AA)
        else:
            for pointFinal in trajet:
                if (pointInitial == None):
                    pointInitial = pointFinal
                else:
                    cv2.arrowedLine(self.imageVirtuelle, pointFinal, pointInitial, (0, 255, 0), 5)
                    pointInitial = pointFinal

    def dessinerDebutFinTrajetPrevu(self, debut, fin):
        debut_x, debut_y = debut
        fin_x, fin_y = fin
        cv2.putText(self.imageVirtuelle, 'Debut', (debut_x - 25, debut_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.imageVirtuelle, 'Fin', (fin_x, fin_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)

