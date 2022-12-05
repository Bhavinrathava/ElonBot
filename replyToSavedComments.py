import praw 
from Common.pymongoGetDb import MongoDBUtility
from Common.subredditScraper import SrScrapper

# Prefect imports
from prefect import task, flow

@flow
def ReplyToComments():
    mongoHelper = MongoDBUtility()


    comments = mongoHelper.getItemsReadOnly("mainDB", "ParsedComments", True)
    reddit = praw.Reddit("elonbot", user_agent="ElonBot v1.0 developed by u/zeroDev_")

    scrapper = SrScrapper()

    comments =  scrapper.sentimentBasedReplies(comments, reddit)
    db = mongoHelper.getDB()

    collection = db["ParsedComments"]

    for comment in comments:
        if(comment['saved']):
            collection.find_one_and_update({'id':comment['id']},{'$set':{'replyID':comment['replyID'].id, 'saved':True}})

if __name__ == "__main__":
    ReplyToComments()