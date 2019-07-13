import socket
import sys
s = socket.socket ()
ip,port,name = sys.argv[1],int(sys.argv[2]),sys.argv[3]
s.connect((ip,port))
print(name)
s.send(bytes(name.encode()))
# Print the received message
print ("Get: to read other clients data. Update: modify your own data")
op = input()

if op == 'get':
	response[op]['name'] = input ()
        s.se
else:
        while response.lower () != 'bye':
   		s.send(bytes(response.encode()))
   		print (s.recv(1024).decode())
   		response = input()
# Send 'bye' also to the server
s.send(bytes(response.encode()))
s.close()
