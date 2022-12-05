from Common.pymongoGetDb import MongoDBUtility
from Common.SentimentAnalysis import Analyser
import bson

# Prefect imports
from prefect import task, flow

@task
def convertCommentToDict(comments):
    data = {}
    # data = {id-> [text]}
    for comment in comments:
        comment = bson.decode(comment.raw)
        print(comment)
        data[comment["commentID"]] = [comment["body"]]
    
    return data

@task
def convertToStorableDict(data):
    parsedData = []

    for key in list(data.keys()):
        arr = data[key]
        parsedData.append({"id":key, "sentiment":arr[1], "replied":False})
    
    return parsedData
@task
def parseSentiment(comments):
    #Do something
    #convert comments to {id->[body]} DS
    data = convertCommentToDict(comments)
    
    #send comments to SA -> [{id->[body,label]}]
    analyser = Analyser()
    data = analyser.classify(data)
    parseSentimentData = convertToStorableDict(data)
    return parseSentimentData

@flow
def parseCommentsFromDB():
        
    mongoHelper = MongoDBUtility()
    comments = mongoHelper.getItemsReadOnly()
    comments = parseSentiment(comments)
    db = mongoHelper.getDB()
    parsedCollection = db["ParsedComments"]
    mongoHelper.storeToCollection(parsedCollection, comments)


if __name__ == "__main__":
    parseCommentsFromDB()
