import urllib.parse
pass1=urllib.parse.quote_plus('nayak')

import pymongo
class Mongo_data():
    def __init__(self):
        client = pymongo.MongoClient("mongodb://dhanu:"+pass1+"@cluster0-shard-00-00.r5smp.mongodb.net:27017,cluster0-shard-00-01.r5smp.mongodb.net:27017,cluster0-shard-00-02.r5smp.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-cd379l-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.db = client['textemo']
        
    def get_user(self):
        col = self.db['userdata']
        return [i for i in col.find()]
    def insert_user(self,username,password):
        d={"username":username,"password":password}
        col = self.db['userdata']
        idx=col.insert_one(d)
        return idx.inserted_id
    def text_feed(self,emotion,text,user):
        col = self.db['textfeed']
        d = {"text":text,'emotion':emotion,"user":user}
        idx = col.insert_one(d)
        return idx.inserted_id
    def get_feedback(self):
        col = self.db['textfeed']
        return [i for i in col.find()]
    def get_login(self,user,password):
        col = self.db['userdata']
        f = col.find_one({"username":user,"password":password})
        if f==None: f=0
        else: f=1
        return f
    def push_org_login(self,user,password):
        col = self.db['userdataact']
        d = {"username":user,"password":password}
        idx = col.insert_one(d)
        return idx.inserted_id