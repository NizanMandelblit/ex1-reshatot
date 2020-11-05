import socket
import sys


serverIP=sys.argv[1]
serverPort=sys.argv[2]



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    print("please enter an adress to search its ip\n enter 'exit' to exit")
    queryToServer=input()
    if queryToServer=='exit':
        break
    s.sendto(str.encode(queryToServer), (serverIP, serverPort))
    data, addr = s.recvfrom(1024)
    print(str(data), addr)

s.close()



