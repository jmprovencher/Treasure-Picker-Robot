import serial

test = serial.Serial('COM7', 9600)
test.write(b'front')