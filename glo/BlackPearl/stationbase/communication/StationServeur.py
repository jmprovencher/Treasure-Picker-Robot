import socket
from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer
import  ConfigPath

verrou = RLock()

class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.monServeur = TCPServer()

    def run(self):
        while 1:
            if (self.doitEnvoyerFichier()):
                try:
                    self.monServeur.sendFile(self.stationBase.myRequest)
                    self.stationBase.envoyerFichier = False
                except:
                    #still not working, getting socket error : only one usage of each socket adress
                    print "Connection with the remote host lost, Trying to reconnect"
                    self.monServeur.closeConnection()
                    self.monServeur = TCPServer()
                    print self.monServeur.connectionEstablished
            elif (self.attenteDuRobot()):
                try:
                    data = self.monServeur.receiveFile()
                except Exception as e:
                    print e
                    #still not working, getting socket error : only one usage of each socket adress
                    print "Connection with the remote host lost, Trying to reconnect"
                    self.monServeur.closeConnection()
                    self.monServeur = TCPServer()
                    print self.monServeur.connectionEstablished

                if data == -1:
                    print('Error while receiving file')
                else:
                    print data
                    commande = data['commande']
                    parametre = data['parametre']
                    if (commande == "termine"):
                        self.stationBase.commandeTermine = True
                        self.stationBase.attente = False

            time.sleep(0.01)

    def doitEnvoyerFichier(self):
        return self.stationBase.envoyerFichier

    def attenteDuRobot(self):
        return self.stationBase.attente


