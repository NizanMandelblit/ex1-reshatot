import socket
import sys
import time

myPort = sys.argv[1]
parentIP = sys.argv[2]
parentPort = sys.argv[3]
ipsFileName = sys.argv[4]  # the cache file

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 12345))

while True:
	f = open(ipsFileName, "a+")
	f.seek(0)
	ipRequest, addrClient = s.recvfrom(1024)
	retLine=None
	#checking the cache of the server
	for x in f:
		lineSplit=x.split(",")
		if ipRequest.decode()==lineSplit[0]:
			retLine=x
	#asking the parent server if its not found in the cache file
	if retLine==None:
		s.sendto(ipRequest,(parentIP,int(parentPort)))
		retLine,addrParentServer=s.recvfrom(1024)
		splitedLine=retLine.decode().split(",")
		f.write('\n'+retLine.decode())
		f.close()
	s.sendto(retLine.encode(), addrClient)



s.close()
