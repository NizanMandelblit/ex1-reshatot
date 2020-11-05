import socket
import sys


myPort=sys.argv[1]
parentIP=sys.argv[2]
parentPort=sys.argv[3]
ipsFileName=sys.argv[4]

f = open(ipsFileName, "r")


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 12346))

while True:
	data, addrClient = s.recvfrom(1024)
	for x in f:
		lineSplit=x.split(",")
		if data.decode()==lineSplit[0]:
			retLine=x
	s.sendto(retLine.encode(), addrClient)


f.close()
s.close()