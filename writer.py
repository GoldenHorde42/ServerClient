import json

class writer:
    use_dict_a = True
    dict_a = {}
    dict_b = {}

    def __init__(cls):
        with open("clientdetails.json") as client:
            cls.dict_a = json.load(client)
            cls.dict_b = cls.dict_a
            cls.flag = True
        client.close()

    @classmethod
    def finduser(cls, username):
        if cls.use_dict_a == True:
            if username in cls.dict_a:
                print("User found!")
                return cls.dict_a[username]
            else:
                print("User not found")
        elif cls.use_dict_a == False:
            if username in cls.dict_b:
                print("User found!")
                return cls.dict_b[username]
            else:
                print("User not found")

    @classmethod
    def writetofile(cls, username, data):
        if cls.use_dict_a == True:
            cls.dict_b[username] = data
            with open("clientdetails.json", 'w') as client:
                json.dump(cls.dict_b, client)
            client.close()
            cls.flag=False
            cls.dict_a[username] = data
        elif cls.flag == False:
            cls.dict_a[username] = data
            with open("clientdetails.json", 'w') as client:
                json.dump(cls.dict_a, client)
            client.close()
            cls.flag=0
            cls.dict_b[username] = data






