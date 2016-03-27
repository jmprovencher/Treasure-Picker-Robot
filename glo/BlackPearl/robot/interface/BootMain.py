import sys
sys.path.append('/home/design3/Desktop/design3/glo/BlackPearl')
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot
import time

def main():
    #monUART = UARTDriver('COM8', 9600) #on Windows
    #monUART = UARTDriver('/dev/ttyACM1', 115200) #on linux
    monUART = None
    robot = Robot(monUART)
    robot.start()

if __name__ == '__main__':
    main()
