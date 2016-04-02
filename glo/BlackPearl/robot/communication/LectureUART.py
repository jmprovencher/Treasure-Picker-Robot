from threading import Thread, RLock

verrou = RLock()


class LectureUART(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot

    def run(self):
        while 1:
            info = self.robot.uartDriver.UART.read(4)
            self.analyserLecture(info)

    def analyserLecture(self, info):
        lettre_manchester = info[0]
        if (info == 'done'):
            self.robot.commandeTerminee = True
        elif (info.count(lettre_manchester) == 4):
            self.robot.lettreObtenue = lettre_manchester
            self.robot.pretEnvoyerLettre = True
        else:
            self.robot.tensionCondensateur = info
