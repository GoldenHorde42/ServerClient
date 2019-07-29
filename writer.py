"""this code ensures that the user receives the latest latest data of any user whenever they please. So we use 2..
... dictionaries and initially, both the dictionaries contain the same data from the json file. Once the user searches...
... for a specific user's data, the data is given from dict a. But, if another user edits dict_a, and updates their own...
.. data, their edit is copied to another variable, and is put into dict_b. Now Dict_b is used for editing and dict_a is for...
... the users who want to read the file data"""

import json
import threading
lock = threading.Lock()
class filewriter:
    use_dict_a = True
    dict_a = {}
    dict_b = {}

    def __init__(cls):
        cls.initialize()


    @classmethod
    def initialize(cls):
        with open("clientdetails.json") as client:
            cls.dict_a = json.load(client)
            cls.dict_b = cls.dict_a
            cls.use_dict_a = True
        print (cls.dict_a)
        print (cls.dict_b)
        client.close()

    @classmethod
    def finduser(cls, username):
        print ('searching for ' + username)
        if cls.use_dict_a == True:
            print('üsing dic a')
            print (cls.dict_a)
            if username in cls.dict_a:
                print("User found!")
                return cls.dict_a[username]
            else:
                return "User not found"
        elif cls.use_dict_a == False:
            print('Using dic b')
            print (cls.dict_b)

            if username in cls.dict_b:
                print("User found!")
                return cls.dict_b[username]
            else:
                return "User not found"

    @classmethod
    def writetofile(cls, username, data):
        #function is locked. Only one thread can access it at a time
        print ('Updating user ' + username + ' with data ' + data)
        lock.acquire()
        if cls.use_dict_a == True:
            cls.dict_b[username] = data
            print (cls.dict_b)
            with open("clientdetails.json", 'w') as client:
                json.dump(cls.dict_b, client)
            client.close()
            cls.use_dict_a=False
            cls.dict_a[username] = data
        elif cls.use_dict_a == False:
            cls.dict_a[username] = data
            print(cls.dict_a)
            with open("clientdetails.json", 'w') as client:
                json.dump(cls.dict_a, client)
            client.close()
            cls.use_dict_a=True
            cls.dict_b[username] = data
        lock.release()





