import sys
import socket
import threading
import queue
#import argparse
import json


# Global variables
# TODO: Create a class to hold all the globals as statics
diction ={}
lck = None
Q = queue.Queue(maxsize = 0)


def loadfromfile():
    with open("clientdetails.json") as client:
        dictionary = json.load(client)
    client.close ()
    return(dictionary)

def writetofile (dictionary):
    with open("clientdetails.json",'w') as client:
        json.dump(dictionary,client)
    client.close ()

def serve():
    
    try:  
           global lck,diction
        
       
           localdiction = diction
           print(diction)
           localObj = Q.get()
           name = localObj.recv(1024).decode ()
        
           print("connected to ", str(name))
           response_str = localObj.recv(1024).decode()
           print("received: ", response_str)
           response = json.loads(response_str)
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
                       if user_to_get in localdiction:
                           print('Located obj: ', localdiction[user_to_get])
                           localObj.send(bytes(localdiction[user_to_get].encode()))
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
                       print('user_data is: ', user_data)
                       print('Operating record: ', name)
                       localdiction[name] = user_data
                       print(localdiction)
                       #if client send a bye then the server disconnects

                       resp_str = localObj.recv(1024).decode()
                       print ('Received: ', resp_str)
                       if resp_str == 'bye':
                           break
                       r1 = json.loads(resp_str)
                       user_data = r1['data']['info']
                       writetofile(localdiction)
                       diction = localdiction
                       #lck.release()
                   print('Client said bye')
               else:
                   print('Invalid operation request: ', response['operation'])
    except socket.error as err:
        print("server is still closing try again in 30 seconds", err) 

def main():     
    try:

        #argparse args(sys.argv)
        global diction,lck
        lck = threading.Lock ()

        diction = loadfromfile ()
        s = socket.socket()
        port = int(sys.argv[1])
        s.bind(('',port))
        print("socket is binded to", port)
        s.listen(5)
        print("socket is listening")
        while True:
            c,addr= s.accept()
            Q.put(c)   
            t1 = threading.Thread(target = serve)
            t1.start ()

        c.close ()
    except socket.error as err:
        print("server is still closing try again in 30 seconds", err) 

if __name__ == "__main__":
    main ()

