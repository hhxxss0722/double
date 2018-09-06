import sys
import os
import time
import socket
import hashlib
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(('124.207.149.200', 5001))
sock.connect(('127.0.0.1', 5001))
#sock.send("GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % ('/', '127.0.0.1'))
#data = sock.recv(80960)
#print data

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

try:

    #url  = ("GET %s%s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nRange: bytes=1-357\r\nConnection: keep-alive\r\n\r\n" % ('/', '/TBV0011201703271522.bin', '124.207.149.200:5001'))
    #url  = ("GET %s%s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nRange: bytes=0-35\r\nConnection: keep-alive\r\n\r\n" % ('/', '/zhaocha.py', '124.207.149.200:5001'))
    #url = "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % ('/', '127.0.0.1')
    url = "GET /zone-ws/ws/0.1/terminalZone/getUpgradeAndDataUrlByImei?imei=868986020790466 HTTP/1.1\r\nHost: 124.207.149.200:5001\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n"
    #url = "GET /jiangxi-tcm-ice/ws/0.1/software/versions?imei=868986020790466&master=00006&cm3=00006&masterBoot=C2H01044504B00074529&cm3Boot=01.0002 HTTP/1.1\r\nHost: 124.207.149.200:5001\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n"
    #url = "GET /software/download/TBV0011201703271522?imei=868986020790466 HTTP/1.1\r\nHost: 124.207.149.200:5001\r\nAccept: */*\r\nRange: bytes=0-35\r\nConnection: keep-alive\r\n\r\n"
    print url
    sock.send(url)
    #time.sleep(0.05)
    #len1 = 10
    len2 = 0
    i = 0
    #f = open(r"D:\Svn\svn_lx\DevelopDesign\Python\Code\Scriptlets\test\12.py","w")
    while(1):
        data = sock.recv(4096)
        print "data1:", data
        if 'Content-Length: ' in data:
            index = data.find("Content-Length: ")
            end = data.find("\r\n", index)
            len1 = int(data[index+16:end])
            start = data.find("\r\n\r\n", end)

            len1 = len1 - len(data[start+4:])
            #f.write(data[start+4:].replace("\r\n", "\n"))
            while(len1>1):

                data = sock.recv(2048)
                #f.write(data.replace("\r\n", "\n"))
                print "data2:", data
                print i,len(data),len1
                len1 = len1 - len(data)
                #time.sleep(0.2)
                i += 1

            break
        if '404' in data:
            print '404'
            sys.exit()
        if '301' in data:
            print '301'
            sys.exit()

        #print i
        time.sleep(0.2)
        i += 1
except Exception,ex:
    print Exception,ex
finally:

    sock.close()
    #f.close()
    pwd = os.getcwd()
    print GetFileMd5(pwd + "\\" + "TBV0011201703271522.bin")


