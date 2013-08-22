import socket
import binascii
import os
import sys

broadcast_ip = '192.168.1.255' #change your brodcast adress here
#broadcast_ip = '255.255.255.255' #for some hardware cards broadcast must be this

def wol():
    #mac= "00:1f:d0:25:1c:7c"
    mac= "00:1f:d0:25:28:4d" #change your mac adress here

    mac=mac.replace(':',"")
    mac = binascii.unhexlify(mac)
    print "mac :",binascii.hexlify(mac)


    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto('\xff'*6+mac*16, (broadcast_ip, 0))
    s.sendto('\xff'*6+mac*16, (broadcast_ip, 7))
    s.sendto('\xff'*6+mac*16, (broadcast_ip, 9))
    s.close()
    raw_input("Type [ENTER]")

if __name__ == "__main__":
    wol()
