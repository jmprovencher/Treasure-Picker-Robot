import cv2
from threading import Thread
import time


class TensionCondensateurRobot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.tension = '0V'

    def run(self):
        while 1:
            #call UART et recoit le voltage qu'on enregistre dans self.tension
            #self.tension = bon voltage ## On ira chercher ici l'info sur la tension
            #pour l'instant, on recoit des commandes de la station pour le robot.
            
            time.sleep(0.2)