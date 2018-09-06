#!/usr/bin/python
#coding=utf-8
import threading, logging, socket

DATEFMT = "%H:%M:%S"
FORMAT = "[%(asctime)s]\t [%(threadName)s,%(thread)d] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)

sock = socket.socket()
addr = ('127.0.0.1', 9995)
event = threading.Event()

sock.bind(addr)
sock.listen(5)


def _accept(sock):
    s, addrinfo = sock.accept()
    f = s.makefile(mode='rw')

    while True:
        line = f.readline()  # read(10) 文本使用readline
        logging.info(line)

        if line.strip() == 'quit':
            break

        msg = "Your msg = {}. ack".format(line)
        f.write(msg)
        f.flush()
    f.close()
    sock.close()

threading.Thread(target=_accept, args=(sock,)).start()

while not event.wait(2):
    print event.wait()
    logging.info(sock)