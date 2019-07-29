import socket
import sys
import json
import ssl
import argparse
s = socket.socket ()
wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
response = {}
response['data'] = {}
parser = argparse.ArgumentParser('Client program for the tracker.')
parser.add_argument('--port', help='Port where the server runs', required = True )
parser.add_argument('--ip', help='Host IP where the server runs', required = True )
parser.add_argument('--name', help='Name of the user', required= True)

args = parser.parse_args()
port = int(args.port)
ip = args.ip
name = args.name
wrappedSocket.connect((ip,port))
print(name)
response['name'] = name
#s.send(bytes(name.encode()))
# Print the received message
print ("Get: to read other clients data. Update: modify your own data")
response['operation'] = input()

if response['operation'].lower() == 'get':
    print('ënter the name of the client who details you would like to see')
    response['data']['name'] = input ()
    print(response)
    r1 = json.dumps(response)
    wrappedSocket.send(r1.encode())
    r2 = wrappedSocket.recv(1024)
    print('Got: ', r2.decode())
elif response['operation'].lower() == 'update':
        print ('Update selected. Please enter the location info:')
        response['data']['info'] = input ()
        while response['data']['info'].lower () != 'bye':
   	        r1 = json.dumps(response)
   	        print('Sending: ', r1)
   	        wrappedSocket.send(bytes(r1.encode()))
   	        print ("Type bye to end connection with server and anything else to continue conversation")
   	        response['data']['info'] = input()
# Send 'bye' also to the server
r1 = json.dumps(response)
print('Sending bye: ', r1)
wrappedSocket.send(bytes(r1.encode()))
wrappedSocket.close()
