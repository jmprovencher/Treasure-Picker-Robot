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
        self.monClient = TCPClient()

    def run(self):
        while not (self.tacheTerminee()):
            while 1:
                print("Robot Client running")
                try:
                    data = self.monClient.receiveFile()
                    break
                except Exception as e:
                    print e
                    print "Connection Lost, Trying to reconnect"
                    time.sleep(1)
                    self.monClient = TCPClient()

            if data == -1:
                print('Error while receiving file')
            else:
                print data
                commande = data['commande']
                parametre = data['parametre']

                #self.robot.traiterCommande(commande, parametre)
                #monUart.sendCommand(commande, parametre)

                time.sleep(30)
                myRequest = RequeteJSON("termine", 0)
                while 1:
                    try:
                        self.monClient.sendFile('data.json')
                        break
                    except Exception as e:
                        print e
                        print "Connection Lost, Trying to reconnect"
                        time.sleep(1)
                        self.monClient = TCPClient()

    def tacheTerminee(self):
        with verrou:
            return self.robot.tacheTerminee