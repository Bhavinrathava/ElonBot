import praw
from Common.subredditScraper import SrScrapper
import logging
from Common.pymongoGetDb import MongoDBUtility

# Prefect imports
from prefect import task, flow

@task
def assertDataTypes(datadict):
    keys = list(datadict.keys())

    for key in keys:
        if(type(key) !=datadict[key]):
            return False
    
    return True

@task
def parseDownloadedComments(commentList):
    dataset = []
    for comment in commentList:
        datadict = {comment.id:str, comment.body:str, comment.parent_id:str, comment.submission.id:str, comment.subreddit_id:str}
        if(assertDataTypes(datadict)):
            d = {"commentID" : comment.id, "body":comment.body, "parentID":comment.parent_id, "submission":comment.submission.id, "subreddit":comment.subreddit_id}
            dataset.append(d)
        
    return dataset

    

@flow
def SaveCommentstoDB():

    reddit = praw.Reddit("elonbot", user_agent="ElonBot v1.0 developed by u/zeroDev_")
    scrapper = SrScrapper()
    matchingComment = scrapper.findInSubreddit(reddit, "memes", "elon")
    rawData = parseDownloadedComments(matchingComment)
    logging.info("Ready to store {} new records", len(rawData))
    dbhelper = MongoDBUtility()
    collection = dbhelper.getCollection()
    result = collection.insert_many(rawData)
    logging.info(result)

if __name__ == "__main__":
    SaveCommentstoDB()

