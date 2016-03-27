from UARTDriver import UARTDriver
from TCPClient import TCPClient
from threading import Thread, RLock
import time
from robot.communication.RequeteJSON import RequeteJSON

verrou = RLock()

class RobotClient(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.termineeAEteEnvoyerAStation = True
        self.monClient = TCPClient()

    def run(self):
        while not (self.robot.tacheTerminee):
            print("Robot Client running")
            self.envoyerPretAStation()
            while 1:
                if (self.termineeAEteEnvoyerAStation):
                    data = self.attendreCommande()
                    self.traiterCommande(data)
                else:
                    if (self.robot.commandeTerminee):
                        self.envoyerTension()
                        self.envoyerCommandeTerminee()
                    else:
                        self.envoyerTension()
                        time.sleep(0.1)

    def attendreCommande(self):
        while 1:
            try:
                data = self.monClient.receiveFile()
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient()
        if data == -1:
            print('Error while receiving file')

        self.termineeAEteEnvoyerAStation = False
        return data

    def traiterCommande(self, data):
        print data
        commande = data['commande']
        parametre = data['parametre']
        self.robot.traiterCommande(commande, parametre)
        self.termineeAEteEnvoyerAStation = False

    def envoyerTension(self):
        myRequest = RequeteJSON("tension", self.robot.tensionCondensateur)
        while 1:
            try:
                self.monClient.sendFile(myRequest)
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient()

    def envoyerCommandeTerminee(self):
        myRequest = RequeteJSON("termine", 0)
        while 1:
            try:
                self.monClient.sendFile(myRequest)
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient()
        self.robot.commandeTerminee = False

    def envoyerPretAStation(self):
        myRequest = RequeteJSON("robotPret", 0)
        while 1:
            try:
                self.monClient.sendFile(myRequest)
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient()
            time.sleep(0.1)