import sys
import socket
import threading
import queue
import json

# Global variables
# TODO: Create a class to hold all the globals as statics
diction = None
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
           global lck
        
       
           localdiction = diction 
           localObj = Q.get()
           name = localObj.recv(1024) 
        
           print("connected to ", str(name.decode()))        
           response = localObj.recv(1024)
           # Response should have an 'operation' field. Look for it.
           if 'operation' in response:
           # If operation says 'get' process accordingly.
               if response['operation'] == 'get':
                   # There should be a 'name' field inside
                   if 'name' in response['data']:
                       user_to_get = response['data']['name']
                       if user_to_get in localdiction:
                           localObj.send(bytes(localdiction[user_to_get]))
                       else:
                           localObj.send(bytes('N/A'.encode()))
                   elif response['operation'] == 'update':
                       
                       lck.acquire()
                       response = localObj.recv(1024).decode()
                       r1 = json.loads(response)
                       info = response['data']['ínfo']
                       while info.lower() != 'bye':
                           localdiction[name] = info
                           #if client send a bye then the server disconnects 

                           response = localObj.recv(1024).decode()
                           r1 = json.loads(response)
                           info = response['data']['ínfo']
                           writetofile(localdiction)
                           diction = localdiction
                           lck.release()
    except socket.error as err:
        print("server is still closing try again in 30 seconds", err) 

def main():     
    try:
        
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
        b.close ()
if __name__ == "__main__":
    main ()

