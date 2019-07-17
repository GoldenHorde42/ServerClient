import socket
import sys
import json
s = socket.socket ()
response = {}
response['data'] = {}
ip,port,name = sys.argv[1],int(sys.argv[2]),sys.argv[3]
s.connect((ip,port))
print(name)
s.send(bytes(name.encode()))
# Print the received message
print ("Get: to read other clients data. Update: modify your own data")
response['operation'] = input()

if response['operation'].lower() == 'get':
    print("ënter the name of the client who details you would like to see")
    response['data']['name'] = input ()
    print(response)
    r1 = json.dumps(response)
    s.send(r1.encode())
    r2 = s.recv(1024)
    print('Got: ', r2.decode())
elif response['operation'].lower() == 'update':
        response['data']['info'] = input ()
        while response['data']['info'].lower () != 'bye':
   	        r1 = json.dumps(response)
   	        print('Sending: ', r1)
   	        s.send(bytes(r1.encode()))
   	        print ("Type bye to end connection with server and anything else to continue conversation")
   	        response['data']['info'] = input()
# Send 'bye' also to the server
r1 = json.dumps(response)
print('Sending bye: ', r1)
s.send(bytes(r1.encode()))
s.close()
