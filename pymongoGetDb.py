
from pymongo import MongoClient

class MongoDBUtility:
    def __init__(self,uri = "mongodb+srv://cluster0.ub5ozyl.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority", certPath ='./certs/X509-cert-1214252752964541086.pem',tls = True  ) -> None:
        self.uri = uri
        self.certPath = certPath
        self.tls = tls
        self.client = None

    def getConnection(self):
        self.client = MongoClient(self.uri,
                     tls=self.tls,
                     tlsCertificateKeyFile=self.certPath)

    def getCollection(self, dbName = "mainDB", collectionName = "redditComments"):
        if(self.client is None):
            self.getConnection()
            db = self.client[dbName]
            collection = db[collectionName]
            return collection 

    


        
