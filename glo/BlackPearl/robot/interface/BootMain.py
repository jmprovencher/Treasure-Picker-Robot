import sys
sys.path.append('/home/design3/Desktop/design3/glo/BlackPearl')
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot
import time

def main():
    monUART = UARTDriver('/dev/ttyACM0', 115200) #on linux
    monUART = None
    robot = Robot(monUART)
    robot.start()

if __name__ == '__main__':
    main()
