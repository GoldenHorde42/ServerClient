import socket
import sys
s = socket.socket ()
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
    r1 = json.dumps(response, sort_keys=False, indent=2)
    s.send(r1.encode())

elif response['operation'].lower() == 'update':
        response['data']['info'] = input ()
        while response['data']['info'].lower () != 'bye':
   		s.send(bytes(response.encode()))
   		print ("Type bye to end connection with server and anything else to continue conversation")
   		response['data']['info'] = input()
# Send 'bye' also to the server
s.send(bytes(response.encode()))
s.close()
