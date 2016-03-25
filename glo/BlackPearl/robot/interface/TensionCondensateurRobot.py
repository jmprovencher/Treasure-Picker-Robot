import cv2
from threading import Thread
import time
from robot.communication.RequeteVoltageJSON import RequeteVoltageJSON


class TensionCondensateurRobot(Thread):
    def __init__(self, uartDriver):
        Thread.__init__(self)
        self.uartDriver = uartDriver
        self.tension = '0V'
        self.voltage

    def run(self):
        while 1:
            #call UART et recoit le voltage qu'on enregistre dans self.tension
            #self.tension = bon voltage ## On ira chercher ici l'info sur la tension
            #pour l'instant, on recoit des commandes de la station pour le robot.
            self.voltage = self.uartDriver.T.read(4)


            time.sleep(1)