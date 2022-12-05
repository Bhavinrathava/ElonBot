
from pymongo import MongoClient
from bson.raw_bson import RawBSONDocument

# Prefect imports
from prefect import task, flow

class MongoDBUtility:
    def __init__(self,uri = "mongodb+srv://cluster0.ub5ozyl.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority", certPath ='./certs/X509-cert-1214252752964541086.pem',tls = True  ) -> None:
        self.uri = uri
        self.certPath = certPath
        self.tls = tls
        self.client = None

    @task
    def getConnection(self):
        self.client = MongoClient(self.uri,
                     tls=self.tls,
                     tlsCertificateKeyFile=self.certPath)
    @task
    def getCollection(self, dbName = "mainDB", collectionName = "redditComments"):
        if(self.client is None):
            self.getConnection()
            db = self.client[dbName]
            collection = db[collectionName]
            return collection 
    @task
    def getItemsReadOnly(self, dbName="mainDB", collectionName="redditComments",findRepliedpending = False):
        collection = self.getCollection(dbName, collectionName)
        raw_coll = collection.with_options(codec_options=collection.codec_options.with_options(document_class=RawBSONDocument))
        if(findRepliedpending):
            return raw_coll.find({'saved':False})
        return raw_coll.find({})

    @task
    def storeToCollection(self, collection, items):
        if(collection is not None and len(items)>0):
            collection.insert_many(items)
    @task
    def getDB(self, dbName = "mainDB"):
        if(self.client is None):
            self.getConnection
        
        return self.client[dbName]
        




    


        
