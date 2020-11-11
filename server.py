import socket
import sys
import time

#time_start = time.time()
seconds = 0
myPort = sys.argv[1]
parentIP = sys.argv[2]
parentPort = sys.argv[3]
ipsFileName = sys.argv[4]  # the cache file

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(myPort)))

while True:
	f = open(ipsFileName, "a+")
	f.seek(0)
	ipRequest, addrClient = s.recvfrom(1024)
	retLine=None

	#checking the cache of the server
	for x in f:
		lineSplit=x.split(",")
		if ipRequest.decode()==lineSplit[0]:
			if len(lineSplit)== 3: # static
				retLine=x
				break
			else:  # learned from parent
				ttl=lineSplit[2]
				savedAt = float(lineSplit[3])
				seconds = int(time.time() - savedAt)
				print("seconds:"+str(seconds))
				if int(ttl)>= seconds:
					retLine=x
				else:
					print("too much time is spent!")
					retLine=None

	#  asking the parent server if its not found in the cache file
	if retLine==None:
		s.sendto(ipRequest,(parentIP,int(parentPort)))
		retLine,addrParentServer=s.recvfrom(1024) # we learn retLine from the parent server
		retLine = retLine.decode()
		splittedRetLine = retLine.split(",")
		if len(splittedRetLine) == 3:
			retLine = retLine[:len(retLine) - 1]
			retLine += "," + str(int(time.time())) + "\n" # ? "\n"
		else:  # there is "time.time() already and we need to replace it
			splittedRetLine[3] = str(int(time.time())) + "\n"
			retLine = splittedRetLine[0] + "," + splittedRetLine[1] + "," + splittedRetLine[2] + "," + splittedRetLine[3]
		# retLine = retLine[:len(retLine) - 1]
		# retLine += "," + str(int(time.time())) + "\n" # ? "\n"
		#splitedLine=retLine.split(",")
		f.write(retLine) # always at the end of the file
		f.close()
	s.sendto(retLine.encode(), addrClient)



# s.close() ?
