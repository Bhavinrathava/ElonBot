import praw 
from Common.pymongoGetDb import getDB, getItemsReadOnly
from Common.subredditScraper import sentimentBasedReplies

# Prefect imports
from prefect import task

@task(name = "Replying to comments")
def ReplyToComments():
    comments = getItemsReadOnly("mainDB", "ParsedComments", True) #[{id:ID, Sentiment: SENTIMENT}, ..]
    reddit = praw.Reddit("elonbot", user_agent="ElonBot v1.0 developed by u/zeroDev_")
    comments =  sentimentBasedReplies(comments, reddit)
    collection = getDB()["ParsedComments"]

    for comment in comments:
        if(comment['replied']):
            collection.find_one_and_update({'commentID':comment['commentID']},{'$set':{'replyID':comment['replyID'], 'replied': True}})

if __name__ == "__main__":
    ReplyToComments()