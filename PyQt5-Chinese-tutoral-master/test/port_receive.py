import serial
import time

receive_port = serial.Serial()
print(receive_port)
try:
    ser = serial.Serial('COM7',115200,timeout=60)
except Exception as e:
    raise IOError("Could not open port: %s" % e)
print(ser.port)

while 1:
    data = ser.read(1024).decode().strip()
    if len(data) == 0 or data == '/r/n' or data == '\n':
        continue
    else:
        print(data)
