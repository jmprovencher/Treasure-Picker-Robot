from UARTDriver import UARTDriver
from TCPClient import TCPClient
from threading import Thread, RLock

class RobotClient(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.monClient = TCPClient()

    def run(self):
        while 1:
            print("RobotClient run")
            try:
                data = self.monClient.receiveFile()
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
                self.monClient = TCPClient()

        if data == -1:
            print('Error while receiving file')
        else:
            print data
            commande = data['commande']
            parametre = data['parametre']
            self.robot.traiterCommande(commande, parametre)
            #monUart.sendCommand(commande, parametre)