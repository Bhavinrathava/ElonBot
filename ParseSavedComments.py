from Common.pymongoGetDb import getDB, getItemsReadOnly, storeToCollection
from Common.SentimentAnalysis import classify
import bson

# Prefect imports
from prefect import task

@task(name = "Parsing Saving comments from Mongo")
def parseCommentsFromDB():
    comments = getItemsReadOnly()  # [{id: ID, Body: body},..]
    comments = classify(comments)
    parsedCollection = getDB()["ParsedComments"]
    storeToCollection(parsedCollection, comments)

if __name__ == "__main__":
    parseCommentsFromDB()
