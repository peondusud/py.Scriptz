#!/usr/bin/env python
import socket
import binascii
import os
import sys

def wol():
	#### params ####
	macs= ( "00:1f:d0:25:1c:7c", "00:1f:d0:25:28:4d" ) #change your mac adress here
	broadcast_ips = ( '192.168.1.255' , '255.255.255.255' ) #change your brodcast adress here
	ports = ( 0 , 7 , 9 )
	################
	
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	for broadcast_ip in broadcast_ips:
		for mac in macs:
			macz=mac.replace(':',"")
			macz = binascii.unhexlify(macz)
			print "Broadcast addr :",broadcast_ip,"\n\tmac :",mac
			print
			for port in ports:
				s.sendto('\xff'*6+macz*16, (broadcast_ip, port))
	s.close()

if __name__ == "__main__":
	wol()
	raw_input("Type [ENTER]")
