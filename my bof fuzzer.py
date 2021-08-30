#!/usr/bin/python

import socket
from struct import pack


def fuzz():
    try:
        for i in range(0, 1000, 100):

            buffer = "A"*i
            
            print("Fuzzing %s bytes" % i)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 42424))
            print (buffer)
            s.send(bytes(buffer + "\r\n","utf-8"))
            breakpoint()
            s.close()
    except:
        print("Impossibile stabilire la connessione")

fuzz()