import sys
import ssl
import socket
import threading
import queue
import argparse
import json
from writer import filewriter

# Global variables
# TODO: Create a class to hold all the globals as statics
diction ={}
lck = None
Q = queue.Queue(maxsize = 0)

def serve():
    
    try:  

           #get client from queue
           localObj = Q.get()
           print ('Looking for packets in ' + str(localObj.getsockname()))
           #recieve his name,operation and data to be updated/userdata to found
           response_str = localObj.recv(1024).decode()

           print("received: ", response_str)
           response = json.loads(response_str)
           name = response['name']
           print("connected to ", response['name'])
           print("after json loading: ", response)
           # Response should have an 'operation' field. Look for it.
           if 'operation' in response:
           # If operation says 'get' process accordingly.
               print("Operation is: ", response['operation'])
               if response['operation'] == 'get':
                   # There should be a 'name' field inside
                   print('Responding to get')
                   if 'name' in response['data']:
                       user_to_get = response['data']['name']
                       print('Looking for user: ', user_to_get)
                       a = filewriter.finduser(user_to_get)
                       if a != "User not found":
                           print('Located obj: ', a)
                           localObj.send(bytes(a.encode()))
                       else:
                           print('Could not get user: ', user_to_get)
                           localObj.send(bytes('N/A'.encode()))
               elif response['operation'] == 'update':
                   print('Operation is: ', response['operation'])
                   #lck.acquire()
                   #print("still working")
                   print ('Data is: ', response['data'])
                   user_data = response['data']['info']

                   while user_data.lower() != 'bye':
                       user_data1 = user_data
                       print('user_data is: ', user_data)
                       #print('Operating record: ', name)

                       #if client send a bye then the server disconnects

                       resp_str = localObj.recv(1024).decode()
                       print ('Received: ', resp_str)
                       if resp_str == 'bye':
                           break
                       r1 = json.loads(resp_str)
                       user_data = r1['data']['info']

                   filewriter.writetofile(name, user_data1)
                   print('Client said bye')
               else:
                   print('Invalid operation request: ', response['operation'])
    except socket.error as err:
        print("server is still closing try again in 30 seconds", err) 

def main():     
    try:

        #argparse args(sys.argv)

        obj = filewriter ()
        s = socket.socket()
        wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
        parser = argparse.ArgumentParser()
        parser.add_argument('--port',required = True)

        args = parser.parse_args()
        port = int(args.port)
        wrappedSocket.bind(('',port))
        print("socket is binded to", port)
        wrappedSocket.listen(5)
        print("socket is listening")
        while True:
            c,addr= wrappedSocket.accept()
            Q.put(c)
            print ('Launching thread for ' + str(addr))
            t1 = threading.Thread(target = serve)
            t1.start ()

        c.close ()
    except socket.error as err:
        print("server is still closing try again in 30 seconds", err) 

if __name__ == "__main__":
    main ()

