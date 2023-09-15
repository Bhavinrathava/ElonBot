
from pymongo import MongoClient
from bson.raw_bson import RawBSONDocument

# Prefect imports
from prefect import task, flow

def getConnection():
    return MongoClient("mongodb+srv://bhavinmongocluster.5t6smyb.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
                    tls=True,
                    tlsCertificateKeyFile='./certs/X509-cert-3399431802601370317.pem')

def getCollection(dbName = "mainDB", collectionName = "redditComments"):
        return getConnection()[dbName][collectionName]
        

def getItemsReadOnly(dbName="mainDB", collectionName="redditComments",findRepliedpending = False):
    collection = getCollection(dbName, collectionName)

    results = None
    lookFor = ""
    idTag = "commentID"
    if(findRepliedpending):
        results = collection.find({'replied':False})
        lookFor = 'sentiment'
    else:
        results = collection.find({})
        lookFor = 'body'

    data = []
    # data = {id-> [text]}
    for comment in results:
         data.append({idTag : comment[idTag], lookFor : comment[lookFor]})
    return data


def storeToCollection(collection, items):
    if(collection is not None and len(items)>0):
        collection.insert_many(items)


def getDB(dbName = "mainDB"):
    return getConnection()[dbName]
    







        
