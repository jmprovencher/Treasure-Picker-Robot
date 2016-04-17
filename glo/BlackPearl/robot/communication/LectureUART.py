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
        if (isinstance(info, str)):
            lettre_manchester = info[0]
            if info == 'done':
                self.robot.commandeTerminee = True
            elif info.count(lettre_manchester) == 4:
                self.robot.lettreObtenue = lettre_manchester
        elif (isinstance(info, float)):
            self.robot.tensionCondensateur = info
        else:
            print("Resend data")
