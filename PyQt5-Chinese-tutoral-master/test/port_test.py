import serial.tools.list_ports as getport
import serial
import os
import xml.etree.ElementTree as et
import codecs,re

com = serial.Serial()
# com.open()
# print('com = ',str(com))
# com.write('111111'.encode('utf-8'))
port_list = list(getport.comports())
print('port_list = ' + str(port_list))
for e in port_list:
    print('e = '+ str(e))
    # e.write('000000'.encode("utr-8"))
serial_name = port_list[0]
serialFd = serial.Serial('COM6', 115200 ,timeout = 60 )
serialFd.write('111111'.encode("utf-8"))
print("available port " + str(serialFd))
path = str(os.path.dirname(os.path.realpath(__file__)))+'\\wifiset.xml'
print('path = ' + str(path))
root = et.parse(path)
p=root.findall('.')
xmllist={}
for oneper in p:
    for child in oneper.getchildren():
        t = [child.tag,child.text]
        xmllist[child.tag] = t
print('xmllist= ' +str(xmllist))