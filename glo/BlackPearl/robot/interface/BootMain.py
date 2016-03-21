from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot


def main():
    #monUART = UARTDriver('COM8', 9600) #on Windows
    #monUART = UARTDriver('/dev/ttyACM0', 9600) #on linux
    robot = Robot(monUART)
    robot.start()


if __name__ == '__main__':
    main()